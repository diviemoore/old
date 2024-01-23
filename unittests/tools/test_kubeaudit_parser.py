from ..dojo_test_case import DojoTestCase
from dojo.tools.Kubeaudit.parser import KubeAuditParser
from dojo.models import Test


class TestKubeAuditParser(DojoTestCase):

    def test_parse_file_has_no_findings(self):
        testfile = open("unittests/scans/drheader/kubeaudit.json")
        parser = KubeAuditParser()
        findings = parser.get_findings(testfile, Test())
        testfile.close()
        self.assertEqual(70, len(findings))