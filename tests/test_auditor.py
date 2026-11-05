import os
import unittest
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from onboard_project import generate_dossier, audit_dossier

class TestDossierAuditor(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_passes_on_fresh_generation(self):
        generate_dossier(self.test_dir, project_name="AuditTestApp")
        audit_res = audit_dossier(self.test_dir)
        self.assertTrue(audit_res["passed"])
        self.assertEqual(len(audit_res["missing_dossiers"]), 0)
        self.assertEqual(len(audit_res["broken_links"]), 0)
        self.assertEqual(len(audit_res["secret_findings"]), 0)

    def test_audit_catches_missing_dossier(self):
        generate_dossier(self.test_dir, project_name="AuditTestApp")
        # Delete one file
        os.remove(os.path.join(self.test_dir, "docs", "CURRENT_STATE.md"))
        audit_res = audit_dossier(self.test_dir)
        self.assertFalse(audit_res["passed"])
        missing_files = [m["file"] for m in audit_res["missing_dossiers"]]
        self.assertIn("docs/CURRENT_STATE.md", missing_files)

    def test_audit_catches_broken_link(self):
        generate_dossier(self.test_dir, project_name="AuditTestApp")
        # Introduce broken link in AGENTS.md
        agents_path = os.path.join(self.test_dir, "AGENTS.md")
        with open(agents_path, "a", encoding="utf-8") as f:
            f.write("\n[Missing Link](docs/DOES_NOT_EXIST.md)\n")

        audit_res = audit_dossier(self.test_dir)
        self.assertFalse(audit_res["passed"])
        self.assertTrue(any("DOES_NOT_EXIST.md" in b["target"] for b in audit_res["broken_links"]))

    def test_audit_catches_secret_leak(self):
        generate_dossier(self.test_dir, project_name="AuditTestApp")
        agents_path = os.path.join(self.test_dir, "AGENTS.md")
        with open(agents_path, "a", encoding="utf-8") as f:
            f.write("\nAPI_KEY = 'AKIA1234567890ABCDEF1234'\n")

        audit_res = audit_dossier(self.test_dir)
        self.assertFalse(audit_res["passed"])
        self.assertTrue(len(audit_res["secret_findings"]) > 0)

if __name__ == "__main__":
    unittest.main()

