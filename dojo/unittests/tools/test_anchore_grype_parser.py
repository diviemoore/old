from django.test import TestCase

from dojo.models import Finding, Test
from dojo.tools.anchore_grype.parser import AnchoreGrypeScanParser


class TestAnchoreEngineParser(TestCase):

    def test_anchore_engine_parser_has_many_findings(self):
        testfile = open("dojo/unittests/scans/anchore_grype/many_vulns.json")
        parser = AnchoreGrypeScanParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(388, len(findings))
        for finding in findings:
            self.assertIn(finding.severity, Finding.SEVERITIES)
            self.assertIsNotNone(finding.cve)
        finding = findings[0]
        self.assertEqual("CVE-2011-3389", finding.cve)
        self.assertEqual("Medium", finding.severity)
        self.assertEqual("libgnutls-openssl27", finding.component_name)
        self.assertEqual("3.6.7-4+deb10u5", finding.component_version)
        self.assertEqual("CVE-2011-3389", finding.vuln_id_from_tool)
