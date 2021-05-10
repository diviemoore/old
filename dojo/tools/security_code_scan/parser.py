import json

from dojo.models import Finding

# Import Result of CLI from SecurityCode Scan
# https://github.com/security-code-scan/security-code-scan
# We need to pass --cwe to the scanner for the data to feed CWE in the report


class SecurityCodeScan(object):

    def get_scan_types(self):
        return ["Security Code Scan Report"]

    def get_label_for_scan_types(self, scan_type):
        return scan_type  # no custom label for now

    def get_description_for_scan_types(self, scan_type):
        return "Import Security Code Scan output (--json)"

    def get_findings(self, filename, test):
        return None