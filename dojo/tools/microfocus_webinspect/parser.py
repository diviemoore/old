from xml.dom import NamespaceErr
import hashlib
import html2text
from urllib.parse import urlparse
import re
from defusedxml import ElementTree as ET
from dojo.models import Endpoint, Finding


class MicrofocusWebinspectXMLParser(object):
    """Micro Focus Webinspect XML report parser"""
    def __init__(self, file, test):
        self.dupes = dict()
        self.items = ()
        if file is None:
            return

        tree = ET.parse(file)
        # get root of tree.
        root = tree.getroot()
        if 'Sessions' not in root.tag:
            raise NamespaceErr("This doesn't seem to be a valid Webinspect xml file.")

        for session in root:
            url = session.find('URL').text
            host = session.find('Host').text
            port = session.find('Port').text
            scheme = session.find('Scheme').text
            issues = session.find('Issues')
            for issue in issues.findall('Issue'):
                title = issue.find('Name').text
                severity = convert_severity(issue.find('Severity').text)
                for content in issue.findall('ReportSection'):
                    name = content.find('Name').text
                    if 'Summary' in name:
                        if content.find('SectionText').text:
                            description = content.find('SectionText').text
                        else:
                            description = ""
                    if 'Fix' in name:
                        if content.find('SectionText').text:
                            mitigation = content.find('SectionText').text
                        else:
                            mitigation = ""
                    if 'Reference' in name:
                        if name and content.find('SectionText').text:
                            reference = html2text.html2text(content.find('SectionText').text)
                        else:
                            reference = ""
                classifications = issue.find('Classifications')
                for content in classifications.findall('Classification'):
                    # detect CWE number
                    # TODO support more than one CWE number
                    if "kind" in content.attrib and "CWE" == content.attrib["kind"]:
                        cwe = get_cwe(content.attrib['identifier'])
                        description += "\n\n" + content.text + "\n"

                # make dupe hash key
                dupe_key = hashlib.md5(str(description + title + severity).encode('utf-8')).hexdigest()
                # check if dupes are present.
                if dupe_key in self.dupes:
                    finding = self.dupes[dupe_key]
                    if finding.description:
                        finding.description = finding.description
                    self.process_endpoints(finding, host)
                    self.dupes[dupe_key] = finding
                else:
                    self.dupes[dupe_key] = True

                    finding = Finding(title=title,
                                    test=test,
                                    active=False,
                                    verified=False,
                                    cwe=cwe,
                                    description=description,
                                    severity=severity,
                                    numerical_severity=Finding.get_numerical_severity(
                                        severity),
                                    mitigation=mitigation,
                                    references=reference,
                                    static_finding=False,
                                    dynamic_finding=True)
                    # manage endpoints
                    parts = urlparse(url)
                    finding.unsaved_endpoints.append(Endpoint(protocol=parts.scheme,
                                                     host=parts.netloc,
                                                     path=parts.path,
                                                     query=parts.query,
                                                     fragment=parts.fragment,
                                                     product=test.engagement.product))
                    self.dupes[dupe_key] = finding

            self.items = list(self.dupes.values())

    @staticmethod
    def convert_severity(val):
        if val == "0":
            return "Info"
        elif val == "1":
            return "Low"
        elif val == "2":
            return "Medium",
        elif val == "3":
            return "High"
        else:
            return "Info"

    @staticmethod
    def get_cwe(val):
        # Match only the first CWE!
        cweSearch = re.search("CWE-(\\d+)", val, re.IGNORECASE)
        if cweSearch:
            return int(cweSearch.group(1))
        else:
            return 0
