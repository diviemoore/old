from dojo.models import Test
from dojo.tools.testssl.parser import TestsslParser

from ..dojo_test_case import DojoTestCase


class TestTestsslParser(DojoTestCase):

    def test_parse_file_with_no_vuln_has_no_finding(self):
        with open("unittests/scans/testssl/defectdojo_no_vuln.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            self.assertEqual(0, len(findings))

    def test_parse_file_with_one_vuln_has_one_finding(self):
        with open("unittests/scans/testssl/defectdojo_one_vuln.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(1, len(findings))

    def test_parse_file_with_many_vuln_has_many_findings(self):
        with open("unittests/scans/testssl/defectdojo_many_vuln.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(100, len(findings))
            # finding 8
            # "cipherlist_AVERAGE","www.defectdojo.org/185.199.110.153","443","LOW","offered","","CWE-310"
            finding = findings[8]
            self.assertEqual("Low", finding.severity)
            self.assertEqual(310, finding.cwe)
            # "LUCKY13","www.defectdojo.org/185.199.110.153","443","LOW","potentially vulnerable, uses TLS CBC ciphers","CVE-2013-0169","CWE-310"
            finding = findings[50]
            self.assertEqual("Low", finding.severity)
            self.assertEqual(310, finding.cwe)
            self.assertEqual(4, len(finding.unsaved_vulnerability_ids))
            self.assertEqual("CVE-2013-0169", finding.unsaved_vulnerability_ids[0])
            self.assertEqual("CVE-2013-0169", finding.unsaved_vulnerability_ids[1])
            self.assertEqual("CVE-2013-0169", finding.unsaved_vulnerability_ids[2])
            self.assertEqual("CVE-2013-0169", finding.unsaved_vulnerability_ids[3])
            self.assertEqual(310, finding.cwe)

    def test_parse_file_with_many_cves(self):
        with open("unittests/scans/testssl/many_cves.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(2, len(findings))
            finding = findings[0]
            self.assertEqual("DROWN", finding.title)
            self.assertEqual("High", finding.severity)
            self.assertEqual(1, len(finding.unsaved_vulnerability_ids))
            self.assertEqual("CVE-2016-0800", finding.unsaved_vulnerability_ids[0])
            self.assertEqual(310, finding.cwe)
            finding = findings[1]
            self.assertEqual("DROWN", finding.title)
            self.assertEqual("High", finding.severity)
            self.assertEqual(1, len(finding.unsaved_vulnerability_ids))
            self.assertEqual("CVE-2016-0703", finding.unsaved_vulnerability_ids[0])
            self.assertEqual(310, finding.cwe)

    def test_parse_file_with_31_version(self):
        with open("unittests/scans/testssl/demo.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(12, len(findings))

    def test_parse_file_with_31_version2(self):
        with open("unittests/scans/testssl/demo2.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(3, len(findings))

    def test_parse_file_with_one_vuln_has_overall_medium(self):
        with open("unittests/scans/testssl/overall_medium.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(2, len(findings))

    def test_parse_file_with_one_vuln_has_overall_critical(self):
        with open("unittests/scans/testssl/overall_critical.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(145, len(findings))

    def test_parse_file_with_one_vuln_has_failed_target(self):
        with open("unittests/scans/testssl/failed_target.csv") as testfile:
            parser = TestsslParser()
            findings = parser.get_findings(testfile, Test())
            for finding in findings:
                for endpoint in finding.unsaved_endpoints:
                    endpoint.clean()
            self.assertEqual(1, len(findings))
