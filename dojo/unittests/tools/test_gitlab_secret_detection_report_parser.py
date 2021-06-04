from os import linesep
from django.test import TestCase
from dojo.tools.gitlab_secret_detection_report.parser import (
    GitlabSecretDetectionReportParser,
)
from dojo.models import Test


class TestGitlabSecretDetectionReportParser(TestCase):
    def test_gitlab_secret_detection_report_parser_with_no_vuln_has_no_findings(self):
        testfile = open(
            "dojo/unittests/scans/gitlab_secret_detection_report/gitlab_secret_detection_report_0_vuln.json"
        )
        parser = GitlabSecretDetectionReportParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(0, len(findings))

    def test_gitlab_secret_detection_report_parser_with_one_vuln_has_one_findings(
        self,
    ):
        testfile = open(
            "dojo/unittests/scans/gitlab_secret_detection_report/gitlab_secret_detection_report_1_vuln.json"
        )
        parser = GitlabSecretDetectionReportParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        first_finding = findings[0]
        self.assertEqual(1, len(findings))
        self.assertEqual(5, first_finding.line)
        self.assertEqual("Critical", first_finding.severity)
        self.assertEqual("README.md", first_finding.file_path)
        self.assertEqual("AKIAIOSFODNN7EXAMPLE", first_finding.references)

    def test_gitlab_secret_detection_report_parser_with_many_vuln_has_many_findings(
        self,
    ):
        testfile = open(
            "dojo/unittests/scans/gitlab_secret_detection_report/gitlab_secret_detection_report_3_vuln.json"
        )
        parser = GitlabSecretDetectionReportParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        for finding in findings:
            for endpoint in finding.unsaved_endpoints:
                endpoint.clean()
        self.assertEqual(3, len(findings))
