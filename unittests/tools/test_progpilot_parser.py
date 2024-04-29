from ..dojo_test_case import DojoTestCase
from dojo.models import Test
from dojo.tools.progpilot.parser import ProgpilotParser


class TestProgpilotParser(DojoTestCase):

    def test_crunch42parser_single_has_many_findings(self):
        testfile = open("unittests/scans/progpilot/progpilot.json")
        parser = ProgpilotParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(8, len(findings))
        with self.subTest(i=0):
            finding = findings[0]
            self.assertEqual("Info", finding.severity)
            self.assertIsNotNone(finding.description)
            self.assertGreater(len(finding.description), 0)
