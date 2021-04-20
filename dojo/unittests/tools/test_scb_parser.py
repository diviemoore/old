from django.test import TestCase
from dojo.tools.scb.parser import SCBParser
from dojo.models import Engagement, Product, Test


class TestSCBParser(TestCase):
    def get_test(self):
        test = Test()
        test.engagement = Engagement()
        test.engagement.product = Product()
        return test

    def test_scb_parser_without_file_has_no_findings(self):
        parser = SCBParser()
        findings = parser.get_findings(None, self.get_test())
        self.assertEqual(0, len(findings))

    def test_scb_parser_with_no_vuln_has_no_findings(self):
        testfile = open("dojo/unittests/scans/scb/scb_zero_vul.json")
        parser = SCBParser()
        findings = parser.get_findings(testfile, self.get_test())
        testfile.close()
        self.assertEqual(0, len(findings))

    def test_scb_parser_with_one_criticle_vuln_has_one_findings(self):
        testfile = open("dojo/unittests/scans/scb/scb_one_vul.json")
        parser = SCBParser()
        findings = parser.get_findings(testfile, self.get_test())
        testfile.close()
        self.assertEqual(1, len(findings))
        self.assertEqual("High", findings[0].severity)

    def test_scb_parser_with_many_vuln_has_many_findings(self):
        testfile = open("dojo/unittests/scans/scb/scb_many_vul.json")
        parser = SCBParser()
        findings = parser.get_findings(testfile, self.get_test())
        testfile.close()
        self.assertEqual(5, len(findings))
        self.assertEqual(findings[0].severity, "Info")
        self.assertEqual(findings[0].title, "ssh")
        self.assertEqual(findings[0].description,
                         "Port 22 is open using tcp protocol.")
        self.assertEqual(
            findings[0].unsaved_endpoints[0].host, "scanme.nmap.org")
        self.assertEqual(findings[0].unsaved_endpoints[0].protocol, "tcp")
        self.assertEqual(findings[0].unsaved_endpoints[0].path, "")
        self.assertEqual(findings[0].unsaved_endpoints[0].port, 22)

    def test_scb_parser_handles_multiple_scan_types(self):
        testfile = open(
            "dojo/unittests/scans/scb/scb_multiple_finding_formats.json")
        parser = SCBParser()
        findings = parser.get_findings(testfile, self.get_test())
        testfile.close()
        self.assertEqual(3, len(findings))
        self.assertEqual(findings[0].title, "WordPress Service")
        self.assertEqual(findings[0].description,
                         "WordPress Service Information")
        self.assertEqual(findings[1].title, "SSH Service")
        self.assertEqual(findings[1].description, "SSH Service Information")
        self.assertEqual(
            findings[2].title, "The anti-clickjacking X-Frame-Options header is not present.")
        self.assertEqual(findings[2].description, None)

    def test_scb_parser_empty_with_error(self):
        with self.assertRaises(ValueError) as context:
            testfile = open("dojo/unittests/scans/scb/empty_with_error.json")
            parser = SCBParser()
            findings = parser.get_findings(testfile, self.get_test())
            testfile.close()
