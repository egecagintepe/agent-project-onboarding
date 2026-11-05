import os
import unittest
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from onboard_project import generate_dossier, DOSSIER_FILES

class TestDossierGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_generates_all_dossier_files(self):
        res = generate_dossier(self.test_dir, project_name="TestApp")
        self.assertEqual(len(res["created_files"]), len(DOSSIER_FILES))
        self.assertEqual(len(res["skipped_files"]), 0)

        for rel_path, _ in DOSSIER_FILES:
            full = os.path.join(self.test_dir, rel_path)
            self.assertTrue(os.path.exists(full), f"Expected file not found: {rel_path}")

    def test_non_destructive_by_default(self):
        # Generate once
        res1 = generate_dossier(self.test_dir, project_name="TestApp")
        self.assertEqual(len(res1["created_files"]), len(DOSSIER_FILES))

        # Generate second time without force: should skip existing files
        res2 = generate_dossier(self.test_dir, project_name="TestApp", force=False)
        self.assertEqual(len(res2["created_files"]), 0)
        self.assertEqual(len(res2["skipped_files"]), len(DOSSIER_FILES))

    def test_force_overwrites(self):
        generate_dossier(self.test_dir, project_name="TestApp")
        res = generate_dossier(self.test_dir, project_name="TestApp", force=True)
        self.assertEqual(len(res["created_files"]), len(DOSSIER_FILES))
        self.assertEqual(len(res["skipped_files"]), 0)

    def test_dry_run_creates_no_files(self):
        empty_dir = tempfile.mkdtemp()
        try:
            res = generate_dossier(empty_dir, project_name="DryRunApp", dry_run=True)
            self.assertTrue(res["dry_run"])
            self.assertEqual(len(res["created_files"]), len(DOSSIER_FILES))
            # Verify no files actually created on disk
            for rel_path, _ in DOSSIER_FILES:
                full = os.path.join(empty_dir, rel_path)
                self.assertFalse(os.path.exists(full), f"File should not have been created in dry-run: {rel_path}")
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
