import hashlib
import logging
import re
import dateutil

from cpe import CPE
from defusedxml import ElementTree
from packageurl import PackageURL

from dojo.models import Finding

logger = logging.getLogger(__name__)


class DependencyCheckParser(object):
    SEVERITY_MAPPING = {
        'info': 'Info',
        'low': 'Low',
        'moderate': 'Medium',
        'high': 'High',
    }

    def add_finding(self, finding, dupes):
        key_str = '|'.join([
            str(finding.cve),
            str(finding.cwe),
            str(finding.file_path).lower()
        ])
        key = hashlib.sha256(key_str.encode('utf-8')).hexdigest()
        if key not in dupes:
            dupes[key] = finding

    def get_filename_and_path_from_dependency(self, dependency, related_dependency, namespace):
        if related_dependency:
            if related_dependency.findtext(namespace + 'fileName'):
                return related_dependency.findtext(namespace + 'fileName'), related_dependency.findtext(namespace + 'filePath')
            else:
                # without filename, it would be just a duplicate finding so we have to skip it. filename is only present for relateddependencies since v6.0.0
                # logger.debug('related_dependency: %s', ElementTree.tostring(related_dependency, encoding='utf8', method='xml'))
                return None, None
        else:
            return dependency.findtext(namespace + 'fileName'), dependency.findtext(namespace + 'filePath')

    def get_component_name_and_version_from_dependency(self, dependency, related_dependency, namespace):
        identifiers_node = dependency.find(namespace + 'identifiers')
        if identifiers_node:
            # analyzing identifier from the more generic to
            package_node = identifiers_node.find('.//' + namespace + 'package')
            if package_node:
                id = package_node.findtext(f'{namespace}id')
                purl = PackageURL.from_string(id)
                purl_parts = purl.to_dict()
                component_name = purl_parts['namespace'] + ':' if purl_parts['namespace'] and len(purl_parts['namespace']) > 0 else ''
                component_name += purl_parts['name'] if purl_parts['name'] and len(purl_parts['name']) > 0 else ''
                component_name = component_name if component_name else None
                component_version = purl_parts['version'] if purl_parts['version'] and len(purl_parts['version']) > 0 else ''
                return component_name, component_version

            # vulnerabilityIds_node = identifiers_node.find('.//' + namespace + 'vulnerabilityIds')
            # if vulnerabilityIds_node:
            #     id = vulnerabilityIds_node.findtext(f'{namespace}id')
            #     cpe = CPE(id)
            #     component_name = cpe.get_vendor()[0] + ':' if len(cpe.get_vendor()) > 0 else ''
            #     component_name += cpe.get_product()[0] if len(cpe.get_product()) > 0 else ''
            #     component_name = component_name if component_name else None
            #     component_version = cpe.get_version()[0] if len(cpe.get_version()) > 0 else None
            #     return component_name, component_version

            cpe_node = identifiers_node.find('.//' + namespace + 'identifier[@type="cpe"]')
            if cpe_node:
                id = cpe_node.findtext(f'{namespace}name')
                cpe = CPE(id)
                component_name = cpe.get_vendor()[0] + ':' if len(cpe.get_vendor()) > 0 else ''
                component_name += cpe.get_product()[0] if len(cpe.get_product()) > 0 else ''
                component_name = component_name if component_name else None
                component_version = cpe.get_version()[0] if len(cpe.get_version()) > 0 else None
                return component_name, component_version

            maven_node = identifiers_node.find('.//' + namespace + 'identifier[@type="maven"]')
            if maven_node:
                maven_parts = maven_node.findtext(f'{namespace}name').split(':')
                # logger.debug('maven_parts:' + str(maven_parts))
                if len(maven_parts) == 3:
                    component_name = maven_parts[0] + ':' + maven_parts[1]
                    component_version = maven_parts[2]
                    return component_name, component_version

        # TODO what happens when there multiple evidencecollectednodes with product or version as type?
        evidence_collected_node = dependency.find(namespace + 'evidenceCollected')
        if evidence_collected_node:
            # <evidenceCollected>
            # <evidence type="product" confidence="HIGH">
            #     <source>file</source>
            #     <name>name</name>
            #     <value>jquery</value>
            # </evidence>
            # <evidence type="version" confidence="HIGH">
            #     <source>file</source>
            #     <name>version</name>
            #     <value>3.1.1</value>
            # </evidence>'
            # will find the first product and version node. if there are multiple it may not pick the best
            # since 6.0.0 howoever it seems like there's always a packageurl above so not sure if we need the effort to
            # implement more logic here
            product_node = evidence_collected_node.find('.//' + namespace + 'evidence[@type="product"]')
            if product_node:
                component_name = product_node.findtext(f'{namespace}value')
                version_node = evidence_collected_node.find('.//' + namespace + 'evidence[@type="version"]')
                if version_node:
                    component_version = version_node.findtext(f'{namespace}value')

                return component_name, component_version

        return None, None

    def get_finding_from_vulnerability(self, dependency, related_dependency, vulnerability, test, namespace):
        dependency_filename, dependency_filepath = self.get_filename_and_path_from_dependency(dependency, related_dependency, namespace)
        # logger.debug('dependency_filename: %s', dependency_filename)

        if dependency_filename is None:
            return None

        tags = []
        name = vulnerability.findtext(f'{namespace}name')
        cwes_node = vulnerability.find(f'{namespace}cwes')
        if vulnerability.find(f'{namespace}cwes'):
            cwe_field = vulnerability.find(f'{namespace}cwes').findtext(f'{namespace}cwe')
        else:
            cwe_field = vulnerability.findtext(f'{namespace}cwe')

        description = vulnerability.findtext(f'{namespace}description')
        # I need the notes field since this is how the suppression is documented.
        notes = vulnerability.findtext(f'.//{namespace}notes')

        cve = name[:28]
        if cve and not cve.startswith('CVE'):
            # for vulnerability sources which have a CVE, it is the start of the 'name'.
            # for other sources, we have to set it to None
            cve = None

        # Use CWE-1035 as fallback
        cwe = 1035  # Vulnerable Third Party Component
        if cwe_field:
            m = re.match(r"^(CWE-)?(\d+)", cwe_field)
            if m:
                cwe = int(m.group(2))

        component_name, component_version = self.get_component_name_and_version_from_dependency(dependency, related_dependency, namespace)

        stripped_name = name
        # startswith CVE-XXX-YYY
        stripped_name = re.sub(r'^CVE-\d{4}-\d{4,7}', '', stripped_name).strip()
        # startswith CWE-XXX:
        stripped_name = re.sub(r'^CWE-\d+\:', '', stripped_name).strip()
        # startswith CWE-XXX
        stripped_name = re.sub(r'^CWE-\d+', '', stripped_name).strip()

        if component_name is None:
            logger.warning("component_name was None for File: {}, using dependency file name instead.".format(dependency_filename))
            component_name = dependency_filename

        # some changes in v6.0.0 around CVSS version information
        # https://github.com/jeremylong/DependencyCheck/pull/2781

        cvssv2_node = vulnerability.find(namespace + 'cvssV2')
        cvssv3_node = vulnerability.find(namespace + 'cvssV3')
        severity = vulnerability.findtext(f'{namespace}severity')
        if not severity:
            if cvssv3_node is not None:
                severity = cvssv3_node.findtext(f'{namespace}baseSeverity').lower().capitalize()
            elif cvssv2_node is not None:
                severity = cvssv2_node.findtext(f'{namespace}severity').lower().capitalize()

        # handle if the severity have something not in the mapping
        # default to 'Medium' and produce warnings in logs
        if severity.strip().lower() not in self.SEVERITY_MAPPING:
            logger.warn(f"Warning: Unknow severity value detected '{severity}'. Bypass to 'Medium' value")
            severity = "Medium"
        else:
            severity = self.SEVERITY_MAPPING[severity.strip().lower()]

        reference_detail = None
        references_node = vulnerability.find(namespace + 'references')

        if references_node is not None:
            reference_detail = ''
            for reference_node in references_node.findall(namespace +
                                                          'reference'):
                name = reference_node.findtext(f"{namespace}name")
                source = reference_node.findtext(f"{namespace}source")
                url = reference_node.findtext(f"{namespace}url")
                reference_detail += '**name**: {0}\n' \
                                     '**source**: {1}\n' \
                                     '**url**: {2}\n\n'.format(name, source, url)

        if related_dependency is not None:
            tags.append("related")

        if vulnerability.tag == "{}suppressedVulnerability".format(namespace):
            if notes is None:
                notes = "Document on why we are suppressing this vulnerability is missing!"
                tags.append("no_suppression_document")
            mitigation = '**This vulnerability is mitigated and/or suppressed:** {}\n'.format(notes)
            mitigation = mitigation + 'Update {}:{} to at least the version recommended in the description'.format(component_name, component_version)

            active = False
            tags.append("suppressed")

        else:
            mitigation = 'Update {}:{} to at least the version recommended in the description'.format(component_name, component_version)
            description += '\n**Filepath**: ' + str(dependency_filepath)
            active = True

        return Finding(
            title=f'{component_name}:{component_version} | {name}',
            file_path=dependency_filename,
            test=test,
            cwe=cwe,
            cve=cve,
            description=description,
            severity=severity,
            mitigation=mitigation,
            tags=tags,
            active=active,
            dynamic_finding=False,
            static_finding=True,
            references=reference_detail,
            component_name=component_name,
            component_version=component_version,
        )

    def get_scan_types(self):
        return ["Dependency Check Scan"]

    def get_label_for_scan_types(self, scan_type):
        return scan_type  # no custom label for now

    def get_description_for_scan_types(self, scan_type):
        return "OWASP Dependency Check output can be imported in Xml format."

    def get_findings(self, filename, test):
        dupes = dict()
        namespace = ''
        content = filename.read()

        scan = ElementTree.fromstring(content)
        regex = r"{.*}"
        matches = re.match(regex, scan.tag)
        try:
            namespace = matches.group(0)
        except:
            namespace = ""

        dependencies = scan.find(namespace + 'dependencies')
        scan_date = None
        if scan.find(f"{namespace}projectInfo"):
            projectInfo_node = scan.find(f"{namespace}projectInfo")
            if projectInfo_node.findtext(f"{namespace}reportDate"):
                scan_date = dateutil.parser.parse(projectInfo_node.findtext(f"{namespace}reportDate"))

        if dependencies:
            for dependency in dependencies.findall(namespace + 'dependency'):
                vulnerabilities = dependency.find(namespace + 'vulnerabilities')
                if vulnerabilities is not None:
                    for vulnerability in vulnerabilities.findall(namespace + 'vulnerability'):
                        if vulnerability:
                            finding = self.get_finding_from_vulnerability(dependency, None, vulnerability, test, namespace)
                            if scan_date:
                                finding.date = scan_date
                            self.add_finding(finding, dupes)

                    for suppressedVulnerability in vulnerabilities.findall(namespace + 'suppressedVulnerability'):
                        if suppressedVulnerability:
                            finding = self.get_finding_from_vulnerability(dependency, None, suppressedVulnerability, test, namespace)
                            if scan_date:
                                finding.date = scan_date
                            self.add_finding(finding, dupes)

                    relatedDependencies = dependency.find(namespace + 'relatedDependencies')
                    if relatedDependencies:
                        for relatedDependency in relatedDependencies.findall(namespace + 'relatedDependency'):
                            finding = self.get_finding_from_vulnerability(dependency, relatedDependency, vulnerability, test, namespace)
                            if finding:  # could be None
                                if scan_date:
                                    finding.date = scan_date
                                self.add_finding(finding, dupes)

        return list(dupes.values())
