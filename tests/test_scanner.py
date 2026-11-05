import os
import unittest
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from onboard_project import scan_project

class TestProjectScanner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scan_python_django_project(self):
        # Create dummy manage.py and requirements.txt
        with open(os.path.join(self.test_dir, "manage.py"), "w") as f:
            f.write("# Django manage.py\n")
        with open(os.path.join(self.test_dir, "requirements.txt"), "w") as f:
            f.write("django>=4.2\npsycopg2-binary\nredis\n")

        res = scan_project(self.test_dir)
        self.assertIn("Python", res["languages"])
        self.assertIn("Django", res["frameworks"])
        self.assertIn("PostgreSQL", res["databases"])
        self.assertIn("Redis", res["databases"])

    def test_scan_typescript_node_project(self):
        with open(os.path.join(self.test_dir, "package.json"), "w") as f:
            f.write('{"name": "test-app", "dependencies": {"express": "^4.18.2", "pg": "^8.0.0"}}\n')
        with open(os.path.join(self.test_dir, "tsconfig.json"), "w") as f:
            f.write("{}\n")

        res = scan_project(self.test_dir)
        self.assertIn("TypeScript", res["languages"])
        self.assertIn("Express", res["frameworks"])

    def test_scan_detects_docker(self):
        with open(os.path.join(self.test_dir, "Dockerfile"), "w") as f:
            f.write("FROM python:3.11\n")
        res = scan_project(self.test_dir)
        self.assertTrue(res["has_docker"])

if __name__ == "__main__":
    unittest.main()

