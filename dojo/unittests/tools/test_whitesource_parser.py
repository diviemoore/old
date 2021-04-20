from os import path

from django.test import TestCase
from dojo.models import Test
from dojo.tools.whitesource.parser import WhitesourceParser


class TestWhitesourceParser(TestCase):

    def test_parse_file_with_no_vuln_has_no_findings(self):
        testfile = open(path.join(path.dirname(__file__), "scans/whitesource_sample/okhttp_no_vuln.json"))
        parser = WhitesourceParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_file_with_one_vuln_has_one_findings(self):
        testfile = open(path.join(path.dirname(__file__), "scans/whitesource_sample/okhttp_one_vuln.json"))
        parser = WhitesourceParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))

    def test_parse_file_with_multiple_vuln_has_multiple_finding(self):
        testfile = open(path.join(path.dirname(__file__), "scans/whitesource_sample/okhttp_many_vuln.json"))
        parser = WhitesourceParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(6, len(findings))

    def test_parse_file_with_multiple_vuln_cli_output(self):
        testfile = open(
            path.join(path.dirname(__file__), "scans/whitesource_sample/cli_generated_many_vulns.json")
        )
        parser = WhitesourceParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(20, len(findings))
