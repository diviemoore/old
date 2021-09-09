from django.test import TestCase
from dojo.tools.spotbugs.parser import SpotbugsParser
from dojo.models import Test


class TestSpotbugsParser(TestCase):

    def test_no_findings(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/no_finding.xml", Test())
        self.assertEqual(0, len(findings))

    def test_parse_many_finding(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        self.assertEqual(81, len(findings))

    def test_find_sast_source_line(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        self.assertEqual(95, test_finding.sast_source_line)

    def test_find_sast_source_path(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        self.assertEqual("securitytest/command/IdentityFunctionCommandInjection.kt", test_finding.sast_source_file_path)

    def test_find_source_line(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        self.assertEqual(95, test_finding.line)

    def test_find_file_path(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        self.assertEqual("securitytest/command/IdentityFunctionCommandInjection.kt", test_finding.file_path)

    def test_description(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        # Test if line 13 is correct
        self.assertEqual(
            "At IdentityFunctionCommandInjection.kt:[lines 20-170]",
            test_finding.description.splitlines()[12]
        )

    def test_mitigation(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        # Test if line 10 is correct
        self.assertEqual(
            "#### Example",
            test_finding.mitigation.splitlines()[9]
        )

    def test_references(self):
        parser = SpotbugsParser()
        findings = parser.get_findings("dojo/unittests/scans/spotbugs/many_findings.xml", Test())
        test_finding = findings[0]
        # Test if line 2 is correct
        self.assertEqual(
            "[OWASP: Top 10 2013-A1-Injection](https://www.owasp.org/index.php/Top_10_2013-A1-Injection)",
            test_finding.references.splitlines()[1]
        )

    def test_version_4_4(self):
        """There was a big difference between version < 4.4.x and after
        The dictionnary is not in the report anymore
        """
        testfile = open("dojo/unittests/scans/spotbugs/version_4.4.0.xml")
        parser = SpotbugsParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(9, len(findings))
        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("DMI_HARDCODED_ABSOLUTE_FILENAME", finding.title)
            self.assertEqual("Boot.java", finding.file_path)
            self.assertEqual(23, finding.line)
            self.assertEqual("High", finding.severity)
        with self.subTest(i=8):
            finding = findings[8]
            self.assertEqual("NM_METHOD_NAMING_CONVENTION", finding.title)
            self.assertIsNone(finding.file_path)  # manage special case where file = 'N/A'
            self.assertIsNone(finding.line)
            self.assertEqual("Medium", finding.severity)
