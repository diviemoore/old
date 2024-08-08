import re
from typing import Any, Optional, Tuple, Union

import cvss.parser
from cpe import CPE
from django.core.exceptions import ImproperlyConfigured

from dojo.models import Endpoint, Finding


#######
# Field parsing helper classes
#######
class FieldType:
    """
    Base class for attribute handlers for parsers. Callable, and calls the .handle() method, which should be implemented
    by subclasses.

    We lose type safety by accepting strings for target names; to try to work around this, the check() method on
    subclasses should check whether the configuration for this object makes sense (or as much sense as can be determined
    when the method is called) and raise an ImproperlyConfigured exception if it does not.
    """
    def __init__(self, target_name):
        self.target_name = target_name

    def handle(self, engine_class, finding, value):
        pass

    def __call__(self, engine_class, finding, value):
        self.handle(engine_class, finding, value)

    def check(self, engine_parser):
        pass


class Attribute(FieldType):
    """
    Class for a field that maps directly from one in the input data to a Finding attribute. Initialized with a Finding
    attribute name, when called sets the value of that attribute to the passed-in value.
    """
    def handle(self, engine_class, finding, value):
        setattr(finding, self.target_name, value)

    def check(self, engine_parser):
        if not hasattr(Finding, self.target_name):
            msg = f"Finding does not have attribute '{self.target_name}.'"
            raise ImproperlyConfigured(msg)


class Method(FieldType):
    """
    Class for a field that requires a method to process it. Initialized with a method name, when called it invokes the
    method on the passed-in engine parser, passing in a Finding and value. It's expected that the method will update
    the Finding as it sees fit (i.e., this class does not modify the Finding)
    """
    def handle(self, engine_parser, finding, value):
        getattr(engine_parser, self.target_name)(finding, value)

    def check(self, engine_parser):
        if not callable(getattr(engine_parser, self.target_name, None)):
            msg = f"{type(engine_parser).__name__} does not have method '{self.target_name}().'"
            raise ImproperlyConfigured(msg)


class BaseEngineParser:
    """
    Parser for data shared by all engines used by AppCheck, as well as data from an unknown/unspecified engine.

    Directly mapped attributes, from JSON object -> Finding attribute:
        * _id -> unique_id_from_tool
        * title -> title
        * description -> description
        * first_detected_at -> date
        * solution -> mitigation
        * cvss_v3_vector -> cvssv3
        * epss_base_score -> epss_score

    Data mapped with a bit of tinkering, JSON object -> Finding attribute:
        * status -> active/false_p/risk_accepted (depending on value)
        * cves -> unsaved_vulnerability_ids (vulnerability_ids)
        * cpe -> component name/version
        * cvss_vector -> severity (determined using CVSS package)
        * notes -> appended to Finding description
        * details -> appended to Finding description

    Child classes can override the _ENGINE_FIELDS_MAP dictionary to support extended/different functionality as so
    desired, without having to change/copy the common field parsing described above.
    """
    SCANNING_ENGINE = "Unknown"

    # Field handling common to all findings returned by AppCheck
    _COMMON_FIELDS_MAP: dict[str, FieldType] = {
        "_id": Attribute("unique_id_from_tool"),
        "title": Attribute("title"),
        "description": Attribute("description"),
        "first_detected_at": Attribute("date"),
        "solution": Attribute("mitigation"),
        "cvss_v3_vector": Attribute("cvssv3"),
        "epss_base_score": Attribute("epss_score"),
        "status": Method("parse_status"),
        "cves": Method("parse_cves"),
        "cpe": Method("parse_components"),
        "cvss_vector": Method("parse_severity"),
        # These should be listed after the 'description' entry; they append to it
        "notes": Method("parse_notes"),
        "details": Method("parse_details")}

    # Field handling specific to a given scanning_engine AppCheck uses
    _ENGINE_FIELDS_MAP: dict[str, FieldType] = {}

    def __init__(self):
        # Do a basic check that the fields we'll process over are valid
        for field_handler in self.get_engine_fields().values():
            field_handler.check(self)

    #####
    # For parsing CVEs
    #####
    CVE_PATTERN = re.compile("CVE-[0-9]+-[0-9]+", re.IGNORECASE)

    def is_cve(self, c: str) -> bool:
        return bool(c and isinstance(c, str) and self.CVE_PATTERN.fullmatch(c))

    def parse_cves(self, finding: Finding, value: [str]) -> None:
        finding.unsaved_vulnerability_ids = [c.upper() for c in value if self.is_cve(c)]

    #####
    # Handles setting various status flags on the Finding
    #####
    def parse_status(self, finding: Finding, value: str) -> None:
        # Possible values (best guess): unfixed (the initial value), fixed, false_positive, and acceptable_risk
        value = value.lower()
        if value == "fixed":
            finding.active = False
        elif value == "false_positive":
            finding.false_p = True
        elif value == "acceptable_risk":
            finding.risk_accepted = True

    #####
    # For severity (extracted from cvss vector)
    #####
    def get_severity(self, value: str) -> Optional[str]:
        if cvss_obj := cvss.parser.parse_cvss_from_text(value):
            severity = cvss_obj[0].severities()[0]
            if severity.lower() != "none":
                return severity
        return None

    def parse_severity(self, finding: Finding, value: str) -> None:
        if severity := self.get_severity(value):
            finding.severity = severity

    #####
    # For parsing component data
    #####
    def parse_cpe(self, cpe_str: str) -> (Optional[str], Optional[str]):
        if not cpe_str:
            return None, None
        cpe_obj = CPE(cpe_str)
        return (
            cpe_obj.get_product() and cpe_obj.get_product()[0] or None,
            cpe_obj.get_version() and cpe_obj.get_version()[0] or None,
        )

    def parse_components(self, finding: Finding, value: [str]) -> None:
        # Only use the first entry
        finding.component_name, finding.component_version = self.parse_cpe(value[0])

    #####
    # For parsing additional description-related entries (notes and details)
    #####
    def format_additional_description(self, section: str, value: str) -> str:
        return f"**{section}**: {value}"

    def append_description(self, finding: Finding, addendum: dict[str, str]) -> None:
        if addendum:
            if finding.description:
                finding.description += "\n\n"
            finding.description += "\n\n".join([self.format_additional_description(k, v) for k, v in addendum.items()])

    def parse_notes(self, finding: Finding, value: str) -> None:
        self.append_description(finding, {"Notes": value})

    def extract_details(self, value: Union[str, dict[str, Union[str, dict[str, [str]]]]]) -> dict[str, str]:
        if isinstance(value, dict):
            return {k: v for k, v in value.items() if k != "_meta"}
        return {"Details": str(value)}

    def parse_details(self, finding: Finding, value: dict[str, Union[str, dict[str, [str]]]]) -> None:
        self.append_description(finding, self.extract_details(value))

    #####
    # For parsing endpoints
    #####
    def get_host(self, item: dict[str, Any]) -> str:
        return item.get("url") or item.get("host") or item.get("ipv4_address") or None

    def parse_port(self, item: Any) -> Optional[int]:
        try:
            int_val = int(item)
            if 0 < int_val <= 65535:
                return int_val
        except (ValueError, TypeError):
            pass
        return None

    def get_port(self, item: dict[str, Any]) -> Optional[int]:
        return self.parse_port(item.get('port'))

    def construct_endpoint(self, host: str, port: Optional[int]) -> Endpoint:
        endpoint = Endpoint.from_uri(host)
        if endpoint.host:
            if port:
                endpoint.port = port
        else:
            endpoint = Endpoint(host=host, port=port)
        return endpoint

    def parse_endpoints(self, item: dict[str, Any]) -> [Endpoint]:
        # Endpoint requires a host
        if host := self.get_host(item):
            port = self.get_port(item)
            return [self.construct_endpoint(host, port)]
        return []

    def set_endpoints(self, finding: Finding, item: Any) -> None:
        endpoints = self.parse_endpoints(item)
        finding.unsaved_endpoints.extend(endpoints)

    # Returns the complete field processing map: common fields plus any engine-specific
    def get_engine_fields(self) -> dict[str, FieldType]:
        return {
            **BaseEngineParser._COMMON_FIELDS_MAP,
            **self._ENGINE_FIELDS_MAP}

    def get_finding_key(self, finding: Finding) -> Tuple:
        return (
            finding.severity,
            finding.title,
            tuple(sorted([(e.host, e.port) for e in finding.unsaved_endpoints])),
            self.SCANNING_ENGINE,
        )

    def parse_finding(self, item: dict[str, Any]) -> Tuple[Finding, Tuple]:
        finding = Finding()
        for field, field_handler in self.get_engine_fields().items():
            # Check first whether the field even exists on this item entry; if not, skip it
            if value := item.get(field):
                field_handler(self, finding, value)
        self.set_endpoints(finding, item)
        # Make a note of what scanning engine was used for this Finding
        self.append_description(finding, {"Scanning Engine": self.SCANNING_ENGINE})
        return finding, self.get_finding_key(finding)
