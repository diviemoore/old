from django.test import TestCase
from dojo.tools.cobalt_api.parser import CobaltApiParser
from dojo.models import Test


class TestCobaltApiParser(TestCase):

    def test_cobalt_api_parser_with_no_vuln_has_no_findings(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_zero_vul.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(0, len(findings))

    def test_cobalt_api_parser_with_many_vuln_has_many_findings(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_many_vul.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(3, len(findings))

    def test_cobalt_api_parser_with_carried_over_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_carried_over.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Missing firewall", finding.title)
        self.assertEqual("2021-06-03", finding.date)
        self.assertEqual("Low", finding.severity)
        self.assertIn("A firewall is...", finding.description)
        self.assertEqual("Be sure to...", finding.mitigation)
        self.assertEqual("Try this...", finding.steps_to_reproduce)
        self.assertEqual("2021-06-05", finding.last_status_update)
        self.assertEqual("S3", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_check_fix_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_check_fix.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Cross Site Scripting", finding.title)
        self.assertEqual("2021-05-11", finding.date)
        self.assertEqual("Medium", finding.severity)
        self.assertIn("A XSS injection attack...", finding.description)
        self.assertEqual("Ensure that...", finding.mitigation)
        self.assertEqual("Do this...", finding.steps_to_reproduce)
        self.assertEqual("2021-05-12", finding.last_status_update)
        self.assertEqual("S2", finding.numerical_severity)
        self.assertEqual("vu_3wXY4bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_invalid_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_invalid.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Low", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-02", finding.last_status_update)
        self.assertEqual("S3", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertFalse(finding.active)
        self.assertTrue(finding.verified)
        self.assertTrue(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_need_fix_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_need_fix.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-04-01", finding.date)
        self.assertEqual("High", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-04-05", finding.last_status_update)
        self.assertEqual("S1", finding.numerical_severity)
        self.assertEqual("vu_2wXY3bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_new_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_new.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Info", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-01", finding.last_status_update)
        self.assertEqual("S4", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertFalse(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_out_of_scope_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_out_of_scope.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Low", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-02", finding.last_status_update)
        self.assertEqual("S3", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertFalse(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertTrue(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_triaging_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_triaging.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Info", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-02", finding.last_status_update)
        self.assertEqual("S4", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertFalse(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_valid_fix_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_valid_fix.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Low", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-03", finding.last_status_update)
        self.assertEqual("S3", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertFalse(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertFalse(finding.risk_accepted)
        self.assertTrue(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)

    def test_cobalt_api_parser_with_wont_fix_finding(self):
        testfile = open("dojo/unittests/scans/cobalt_api/cobalt_api_one_vul_wont_fix.json")
        parser = CobaltApiParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("SQL Injection", finding.title)
        self.assertEqual("2021-01-01", finding.date)
        self.assertEqual("Low", finding.severity)
        self.assertIn("A SQL injection attack...", finding.description)
        self.assertEqual("Ensure this...", finding.mitigation)
        self.assertEqual("Do this than that...", finding.steps_to_reproduce)
        self.assertEqual("2021-01-02", finding.last_status_update)
        self.assertEqual("S3", finding.numerical_severity)
        self.assertEqual("vu_5wXY6bq", finding.unique_id_from_tool)
        self.assertTrue(finding.active)
        self.assertTrue(finding.verified)
        self.assertFalse(finding.false_p)
        self.assertFalse(finding.duplicate)
        self.assertFalse(finding.out_of_scope)
        self.assertTrue(finding.risk_accepted)
        self.assertFalse(finding.is_mitigated)
        self.assertFalse(finding.static_finding)
        self.assertTrue(finding.dynamic_finding)
