import datetime
from os import path

from django.test import SimpleTestCase
from dojo.models import Test
from dojo.tools.veracode.parser import VeracodeParser


class TestVeracodeScannerParser(SimpleTestCase):

    def test_parse_file_with_one_finding(self):
        testfile = open(path.join(path.dirname(__file__), "scans/veracode/one_finding.xml"))
        parser = VeracodeParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))

    def test_parse_file_many_findings_different_hash_code_different_unique_id(self):
        testfile = open(path.join(path.dirname(__file__), "scans/veracode/many_findings_different_hash_code_different_unique_id.xml"))
        parser = VeracodeParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(3, len(findings))
        finding = findings[0]
        self.assertEqual("Medium", finding.severity)
        self.assertEqual(123, finding.cwe)
        self.assertEqual("catname", finding.title)
        self.assertFalse(finding.is_Mitigated)
        self.assertEqual("sourcefilepathMyApp2.java", finding.file_path)
        self.assertEqual(2, finding.line)
        self.assertEqual("app-12345_issue-1", finding.unique_id_from_tool)
        finding = findings[1]
        self.assertEqual("High", finding.severity)
        self.assertIsNone(finding.cwe)
        self.assertEqual("CVE-1234-1234", finding.cve)
        self.assertEqual("Vulnerable component: library:1234", finding.title)
        self.assertFalse(finding.is_Mitigated)

    def test_parse_file_with_multiple_finding(self):
        testfile = open(path.join(path.dirname(__file__), "scans/veracode/many_findings.xml"))
        parser = VeracodeParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(3, len(findings))
        finding = findings[0]
        self.assertEqual("Medium", finding.severity)
        self.assertEqual(123, finding.cwe)
        self.assertEqual("catname", finding.title)
        self.assertFalse(finding.is_Mitigated)
        self.assertEqual("sourcefilepathMyApp.java", finding.file_path)
        self.assertEqual(2, finding.line)
        self.assertEqual("app-1234_issue-1", finding.unique_id_from_tool)
        finding = findings[1]
        self.assertEqual("High", finding.severity)
        self.assertIsNone(finding.cwe)
        self.assertEqual("CVE-1234-1234", finding.cve)
        self.assertEqual("Vulnerable component: library:1234", finding.title)
        self.assertFalse(finding.is_Mitigated)
        finding = findings[2]
        self.assertEqual("High", finding.severity)
        self.assertEqual("CVE-5678-5678", finding.cve)
        self.assertEqual("Vulnerable component: library1:1234", finding.title)
        self.assertFalse(finding.is_Mitigated)

    def test_parse_file_with_multiple_finding2(self):
        testfile = open(path.join(path.dirname(__file__), "scans/veracode/veracode_scan.xml"))
        parser = VeracodeParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(7, len(findings))
        finding = findings[0]
        self.assertEqual("Information Exposure Through Sent Data", finding.title)
        self.assertEqual("Low", finding.severity)
        self.assertEqual(201, finding.cwe)
        self.assertEqual(datetime.datetime(2018, 2, 17, 0, 35, 18), finding.date)  # date_first_occurrence="2018-02-17 00:35:18 UTC"
        finding = findings[1]
        self.assertEqual("Low", finding.severity)
        self.assertEqual(201, finding.cwe)
        self.assertEqual("/devTools/utility.jsp", finding.file_path)
        self.assertEqual(361, finding.line)
        self.assertIsNone(finding.component_name)
        self.assertIsNone(finding.component_version)
        # finding 6
        finding = findings[6]
        self.assertEqual("Medium", finding.severity)
        self.assertEqual("CVE-2012-6153", finding.cve)
        self.assertEqual(20, finding.cwe)
        self.assertEqual("commons-httpclient", finding.component_name)
        self.assertEqual("3.1", finding.component_version)
        self.assertEqual("CVE-2012-6153", finding.unique_id_from_tool)

    def test_parse_file_with_mitigated_finding(self):
        testfile = open(path.join(path.dirname(__file__), "scans/veracode/mitigated_finding.xml"))
        parser = VeracodeParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Medium", finding.severity)
        self.assertTrue(finding.is_Mitigated)
        self.assertEqual(datetime.datetime(2020, 6, 1, 10, 2, 1), finding.mitigated)
        self.assertEqual("app-1234_issue-1", finding.unique_id_from_tool)
