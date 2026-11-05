import json
import os
import subprocess
import sys
import tempfile
import unittest

CLI_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "onboard_project.py")

class TestOnboardProjectCLI(unittest.TestCase):
    def test_scan_cli_json(self):
        project_root = os.path.join(os.path.dirname(__file__), "..")
        cmd = [sys.executable, CLI_PATH, "scan", "--path", project_root, "--json"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("Python", data["languages"])
        self.assertIn("evidence", data)

    def test_generate_cli_dry_run_json(self):
        empty_dir = tempfile.mkdtemp()
        try:
            cmd = [
                sys.executable, CLI_PATH, "generate",
                "--path", empty_dir,
                "--project-name", "CLITestApp",
                "--dry-run",
                "--json"
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(res.returncode, 0)
            data = json.loads(res.stdout)
            self.assertTrue(data["dry_run"])
            self.assertEqual(len(data["created_files"]), 8)
        finally:
            import shutil
            shutil.rmtree(empty_dir, ignore_errors=True)

    def test_audit_dossier_cli_json(self):
        # Generate complete dossier in a temp dir
        temp_dir = tempfile.mkdtemp()
        try:
            gen_cmd = [sys.executable, CLI_PATH, "generate", "--path", temp_dir, "--project-name", "AuditCLIApp"]
            subprocess.run(gen_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

            audit_cmd = [sys.executable, CLI_PATH, "audit-dossier", "--path", temp_dir, "--json"]
            res = subprocess.run(audit_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.assertEqual(res.returncode, 0)
            data = json.loads(res.stdout)
            self.assertTrue(data["passed"])
            self.assertEqual(len(data["missing_dossiers"]), 0)
        finally:
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()

