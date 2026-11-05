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
        created = generate_dossier(self.test_dir, project_name="TestApp")
        self.assertEqual(len(created), len(DOSSIER_FILES))

        for rel_path, _ in DOSSIER_FILES:
            full = os.path.join(self.test_dir, rel_path)
            self.assertTrue(os.path.exists(full), f"Expected file not found: {rel_path}")

    def test_idempotent_generation(self):
        # Generate once
        created1 = generate_dossier(self.test_dir, project_name="TestApp")
        self.assertEqual(len(created1), len(DOSSIER_FILES))

        # Generate again: should not overwrite existing files
        created2 = generate_dossier(self.test_dir, project_name="TestApp")
        self.assertEqual(len(created2), 0)

if __name__ == "__main__":
    unittest.main()
