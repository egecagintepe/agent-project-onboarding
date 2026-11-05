import os
import unittest
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from onboard_project import generate_dossier, scan_project

class TestEvidenceBasedReadiness(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="agent_evidence_test_")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_repository_marks_components_unknown(self):
        # In an empty repo, no component should be marked DETECTED
        generate_dossier(self.test_dir, project_name="EmptyApp")
        current_state_file = os.path.join(self.test_dir, "docs", "CURRENT_STATE.md")
        with open(current_state_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Public API Endpoints must NOT be DETECTED when no API exists
        self.assertIn("| Public API Endpoints | **UNKNOWN** |", content)
        self.assertNotIn("| Public API Endpoints | **DETECTED** |", content)

        # Database and Queue must also be UNKNOWN
        self.assertIn("| Database Persistence | **UNKNOWN** |", content)
        self.assertIn("| Background Task Queue | **UNKNOWN** |", content)
        self.assertIn("| Core Application Backend | **UNKNOWN** |", content)
        self.assertIn("| Automated Test Suite | **UNKNOWN** |", content)

    def test_api_detected_only_when_evidence_exists(self):
        # Create an API route file (e.g. urls.py or routes.py)
        with open(os.path.join(self.test_dir, "urls.py"), "w", encoding="utf-8") as f:
            f.write("urlpatterns = []\n")

        generate_dossier(self.test_dir, project_name="ApiApp")
        current_state_file = os.path.join(self.test_dir, "docs", "CURRENT_STATE.md")
        with open(current_state_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("| Public API Endpoints | **DETECTED** |", content)
        self.assertIn("Route declarations exist", content)

    def test_task_queue_detected_only_when_celery_or_worker_exists(self):
        # Create a celery tasks file
        with open(os.path.join(self.test_dir, "tasks.py"), "w", encoding="utf-8") as f:
            f.write("from celery import shared_task\n")

        generate_dossier(self.test_dir, project_name="QueueApp")
        current_state_file = os.path.join(self.test_dir, "docs", "CURRENT_STATE.md")
        with open(current_state_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("| Background Task Queue | **DETECTED** |", content)
        self.assertIn("Celery", content)

    def test_database_detected_when_manifest_contains_db(self):
        with open(os.path.join(self.test_dir, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write("psycopg2-binary>=2.9\n")

        generate_dossier(self.test_dir, project_name="DbApp")
        current_state_file = os.path.join(self.test_dir, "docs", "CURRENT_STATE.md")
        with open(current_state_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("| Database Persistence | **DETECTED** |", content)
        self.assertIn("PostgreSQL", content)

    def test_test_suite_detected_when_runner_exists(self):
        with open(os.path.join(self.test_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
            f.write("[tool.pytest.ini_options]\nminversion = '6.0'\n")

        generate_dossier(self.test_dir, project_name="PytestApp")
        current_state_file = os.path.join(self.test_dir, "docs", "CURRENT_STATE.md")
        with open(current_state_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("| Automated Test Suite | **DETECTED** |", content)
        self.assertIn("pytest", content)

if __name__ == "__main__":
    unittest.main()
