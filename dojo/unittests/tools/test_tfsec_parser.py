from django.test import TestCase
from dojo.tools.tfsec.parser import TFSecParser
from dojo.models import Test


class TestTFSecParser(TestCase):

    def test_parse_no_findings(self):
        testfile = open("dojo/unittests/scans/tfsec/no_findings.json")
        parser = TFSecParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(0, len(findings))

    def test_parse_one_finding(self):
        testfile = open("dojo/unittests/scans/tfsec/one_finding.json")
        parser = TFSecParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(1, len(findings))

        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("Potentially sensitive data stored in block attribute.", finding.title)
            self.assertEqual("Medium", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertTrue(finding.active)
            self.assertEqual("Don't include sensitive data in blocks", finding.mitigation)
            self.assertEqual("Block attribute could be leaking secrets", finding.impact)
            self.assertEqual("tfsec-test/identity.tf", finding.file_path)
            self.assertEqual(226, finding.line)
            self.assertEqual("general", finding.component_name)
            self.assertEqual("GEN003", finding.vuln_id_from_tool)
            self.assertEqual(1, finding.nb_occurences)

    def test_parse_many_findings(self):
        testfile = open("dojo/unittests/scans/tfsec/many_findings.json")
        parser = TFSecParser()
        findings = parser.get_findings(testfile, Test())
        self.assertEqual(4, len(findings))

        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("Legacy client authentication methods utilized.", finding.title)
            self.assertEqual("High", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertTrue(finding.active)
            self.assertEqual("Use service account or OAuth for authentication", finding.mitigation)
            self.assertEqual("Username and password authentication methods are less secure", finding.impact)
            self.assertEqual("tfsec-test/cluster.tf", finding.file_path)
            self.assertEqual(52, finding.line)
            self.assertEqual("google", finding.component_name)
            self.assertEqual("GCP008", finding.vuln_id_from_tool)
            self.assertEqual(1, finding.nb_occurences)

        with self.subTest(i=1):
            finding = findings[1]
            self.assertEqual("Pod security policy enforcement not defined.", finding.title)
            self.assertEqual("High", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertTrue(finding.active)
            self.assertEqual("Use security policies for pods to restrict permissions to those needed to be effective", finding.mitigation)
            self.assertEqual("Pods could be operating with more permissions than required to be effective", finding.impact)
            self.assertEqual("tfsec-test/cluster.tf", finding.file_path)
            self.assertEqual(52, finding.line)
            self.assertEqual("google", finding.component_name)
            self.assertEqual("GCP009", finding.vuln_id_from_tool)
            self.assertEqual(1, finding.nb_occurences)

        with self.subTest(i=2):
            finding = findings[2]
            self.assertEqual("Shielded GKE nodes not enabled.", finding.title)
            self.assertEqual("High", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertTrue(finding.active)
            self.assertEqual("Enable node shielding", finding.mitigation)
            self.assertEqual("Node identity and integrity can't be verified without shielded GKE nodes", finding.impact)
            self.assertEqual("tfsec-test/cluster.tf", finding.file_path)
            self.assertEqual(52, finding.line)
            self.assertEqual("google", finding.component_name)
            self.assertEqual("GCP010", finding.vuln_id_from_tool)
            self.assertEqual(1, finding.nb_occurences)

        with self.subTest(i=3):
            finding = findings[3]
            self.assertEqual("Potentially sensitive data stored in block attribute.", finding.title)
            self.assertEqual("Medium", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertTrue(finding.active)
            self.assertEqual("Don't include sensitive data in blocks", finding.mitigation)
            self.assertEqual("Block attribute could be leaking secrets", finding.impact)
            self.assertEqual("tfsec-test/identity.tf", finding.file_path)
            self.assertEqual(226, finding.line)
            self.assertEqual("general", finding.component_name)
            self.assertEqual("GEN003", finding.vuln_id_from_tool)
            self.assertEqual(1, finding.nb_occurences)
