import json
from dojo.models import Finding

class WizcliIaCParser:
    def get_scan_types(self):
        return ["Wizcli IaC Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Wizcli IaC Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Wizcli IaC Scan results in JSON file format."

    def parse_rule_matches(self, rule_matches, test):
        findings = []
        for rule_match in rule_matches:
            rule = rule_match["rule"]
            rule_id = rule["id"]
            rule_name = rule["name"]
            severity = rule_match["severity"].lower().capitalize()

            for match in rule_match["matches"]:
                resource_name = match["resourceName"]
                file_name = match["fileName"]
                line_number = match.get("lineNumber", "N/A")
                match_content = match["matchContent"]
                expected = match["expected"]
                found = match["found"]
                file_type = match["fileType"]

                description = (
                    f"**Rule ID**: {rule_id}\n"
                    f"**Rule Name**: {rule_name}\n"
                    f"**Resource Name**: {resource_name}\n"
                    f"**File Name**: {file_name}\n"
                    f"**Line Number**: {line_number}\n"
                    f"**Match Content**: {match_content}\n"
                    f"**Expected**: {expected}\n"
                    f"**Found**: {found}\n"
                    f"**File Type**: {file_type}\n"
                )

                finding = Finding(
                    title=f"{rule_name} - {resource_name}",
                    description=description,
                    severity=severity,
                    file_path=file_name,
                    line=line_number,
                    static_finding=True,
                    dynamic_finding=False,
                    mitigation=None,
                    test=test,
                )
                findings.append(finding)
        return findings
