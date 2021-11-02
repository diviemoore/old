from django.test import TestCase
from dojo.tools.semgrep.parser import SemgrepParser
from dojo.models import Test

FINDING_MITIGATION_TEXT = "javax crypto Cipher.getInstance(\"AES/GCM/NoPadding\");"
FINDING_VULN_ID_TEXT = "java.lang.security.audit.cbc-padding-oracle.cbc-padding-oracle"
FINDING_DESCRIPTION_TEXT = "\t\t\tjavax.crypto.Cipher c = javax.crypto.Cipher.getInstance(\"DES/CBC/PKCS5Padding\");"


class TestSemgrepParser(TestCase):

    def test_parse_empty(self):
        testfile = open("dojo/unittests/scans/semgrep/empty.json")
        parser = SemgrepParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(0, len(findings))

    def test_parse_one_finding(self):
        testfile = open("dojo/unittests/scans/semgrep/one_finding.json")
        parser = SemgrepParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Low", finding.severity)
        self.assertEqual("src/main/java/org/owasp/benchmark/testcode/BenchmarkTest02194.java", finding.file_path)
        self.assertEqual(64, finding.line)
        self.assertEqual(696, finding.cwe)
        self.assertEqual(FINDING_MITIGATION_TEXT, finding.mitigation)
        self.assertEqual(FINDING_VULN_ID_TEXT, finding.vuln_id_from_tool)

    def test_parse_many_finding(self):
        testfile = open("dojo/unittests/scans/semgrep/many_findings.json")
        parser = SemgrepParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(3, len(findings))
        finding = findings[0]
        self.assertEqual("Low", finding.severity)
        self.assertEqual("src/main/java/org/owasp/benchmark/testcode/BenchmarkTest02194.java", finding.file_path)
        self.assertEqual(64, finding.line)
        self.assertEqual(696, finding.cwe)
        self.assertEqual(FINDING_MITIGATION_TEXT, finding.mitigation)
        self.assertEqual(FINDING_VULN_ID_TEXT, finding.vuln_id_from_tool)
        self.assertContains(FINDING_DESCRIPTION_TEXT, finding.description)
        finding = findings[2]
        self.assertEqual("Info", finding.severity)
        self.assertEqual("src/main/java/org/owasp/benchmark/testcode/BenchmarkTest01150.java", finding.file_path)
        self.assertEqual(66, finding.line)
        self.assertEqual(696, finding.cwe)
        self.assertEqual(FINDING_MITIGATION_TEXT, finding.mitigation)
        self.assertEqual(FINDING_VULN_ID_TEXT, finding.vuln_id_from_tool)
        self.assertContains(FINDING_DESCRIPTION_TEXT, finding.description)

    def test_parse_repeated_finding(self):
        testfile = open("dojo/unittests/scans/semgrep/repeated_findings.json")
        parser = SemgrepParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(1, len(findings))
        finding = findings[0]
        self.assertEqual("Low", finding.severity)
        self.assertEqual("src/main/java/org/owasp/benchmark/testcode/BenchmarkTest01150.java", finding.file_path)
        self.assertEqual(66, finding.line)
        self.assertEqual(FINDING_VULN_ID_TEXT, finding.vuln_id_from_tool)
        self.assertEqual(696, finding.cwe)
        self.assertEqual(FINDING_MITIGATION_TEXT, finding.mitigation)
        self.assertEqual(2, finding.nb_occurences)
        self.assertContains(FINDING_DESCRIPTION_TEXT, finding.description)

    def test_parse_many_vulns(self):
        testfile = open("dojo/unittests/scans/semgrep/many_vulns.json")
        parser = SemgrepParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(48, len(findings))
        finding = findings[0]
        self.assertEqual("High", finding.severity)
        self.assertEqual("tasks.py", finding.file_path)
        self.assertEqual(186, finding.line)
        self.assertIsNone(finding.mitigation)
        self.assertEqual("python.lang.correctness.tempfile.flush.tempfile-without-flush", finding.vuln_id_from_tool)
        self.assertContains("                   'xsl-style-sheet': temp.name}", finding.description)
        finding = findings[2]
        self.assertEqual("Low", finding.severity)
        self.assertEqual("utils.py", finding.file_path)
        self.assertEqual(503, finding.line)
        self.assertEqual("python.lang.maintainability.useless-ifelse.useless-if-conditional", finding.vuln_id_from_tool)
        finding = findings[4]
        self.assertEqual("Low", finding.severity)
        self.assertEqual("tools/sslyze/parser_xml.py", finding.file_path)
        self.assertEqual(124, finding.line)
        self.assertEqual(327, finding.cwe)
        self.assertEqual("python.lang.security.insecure-hash-algorithms.insecure-hash-algorithm-md5", finding.vuln_id_from_tool)
        finding = findings[37]
        self.assertEqual("High", finding.severity)
        self.assertEqual("management/commands/csv_findings_export.py", finding.file_path)
        self.assertEqual(33, finding.line)
        self.assertEqual(1236, finding.cwe)
        self.assertEqual("python.lang.security.unquoted-csv-writer.unquoted-csv-writer", finding.vuln_id_from_tool)
