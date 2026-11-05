import os
import unittest
import tempfile
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from onboard_project import validate_safe_target_path

class TestPathSafety(unittest.TestCase):
    def setUp(self):
        self.base_dir = tempfile.mkdtemp(prefix="agent_onboarding_test_")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.base_dir, ignore_errors=True)

    def test_safe_relative_paths_allowed(self):
        safe_path = validate_safe_target_path(self.base_dir, "docs/ARCHITECTURE_MAP.md")
        expected = os.path.abspath(os.path.join(self.base_dir, "docs", "ARCHITECTURE_MAP.md"))
        self.assertEqual(safe_path, expected)

    def test_parent_traversal_rejected(self):
        with self.assertRaises(PermissionError) as ctx:
            validate_safe_target_path(self.base_dir, "../escaped_secret.txt")
        self.assertIn("escapes project root", str(ctx.exception))

    def test_sibling_directory_prefix_collision_rejected(self):
        # Vulnerability scenario:
        # If base is "/tmp/project", a sibling directory "/tmp/project-evil"
        # would satisfy naive `target.startswith(base)` because "/tmp/project-evil".startswith("/tmp/project") is True.
        sibling_evil_rel = f"../{os.path.basename(self.base_dir)}-evil/exploit.txt"
        target_candidate = os.path.abspath(os.path.join(self.base_dir, sibling_evil_rel))

        # Prove naive startswith would have failed as a security boundary:
        self.assertTrue(
            target_candidate.startswith(self.base_dir),
            "Test setup precondition: candidate path must share string prefix to test sibling collision"
        )

        # Verify our robust boundary validation rejects the sibling prefix collision:
        with self.assertRaises(PermissionError) as ctx:
            validate_safe_target_path(self.base_dir, sibling_evil_rel)
        self.assertIn("escapes project root", str(ctx.exception))

    def test_symlink_escape_rejected_if_symlinks_supported(self):
        # Create an outside directory
        outside_dir = tempfile.mkdtemp(prefix="agent_outside_")
        try:
            outside_file = os.path.join(outside_dir, "outside_target.txt")
            with open(outside_file, "w") as f:
                f.write("sensitive data")

            symlink_name = os.path.join(self.base_dir, "symlink_dir")
            try:
                os.symlink(outside_dir, symlink_name, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks not permitted by OS or user privileges")

            # Attempting to resolve a path through the escaping symlink must be blocked
            with self.assertRaises(PermissionError) as ctx:
                validate_safe_target_path(self.base_dir, "symlink_dir/outside_target.txt")
            self.assertIn("escapes project root", str(ctx.exception))
        finally:
            import shutil
            shutil.rmtree(outside_dir, ignore_errors=True)

    def test_direct_symlink_target_rejected(self):
        target_file = os.path.join(self.base_dir, "real_target.txt")
        with open(target_file, "w") as f:
            f.write("hello")

        link_file = os.path.join(self.base_dir, "link_to_target.txt")
        try:
            os.symlink(target_file, link_file)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks not permitted by OS or user privileges")

        # Direct symlink targets are rejected
        with self.assertRaises(PermissionError) as ctx:
            validate_safe_target_path(self.base_dir, "link_to_target.txt")
        self.assertIn("Symlink target", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
