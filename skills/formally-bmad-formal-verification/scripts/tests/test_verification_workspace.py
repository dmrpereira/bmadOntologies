import tempfile
import unittest
from pathlib import Path

import verification_workspace


class VerificationWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_verification(self):
        self.assertEqual(verification_workspace.slugify("   "), "verification")

    def test_create_workspace_writes_reports_and_indexes_companions(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            companion = module_root / "artifacts" / "stories" / "story-1"
            companion.mkdir(parents=True)
            (companion / "manifest.json").write_text("{}", encoding="utf-8")

            result = verification_workspace.create_workspace(module_root, "whole model")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "summary.md").is_file())
            self.assertTrue((workspace / "readiness.md").is_file())
            self.assertEqual(len(result["companions"]), 1)
            self.assertTrue((module_root / "reports" / "latest-verification-summary.md").is_file())


if __name__ == "__main__":
    unittest.main()
