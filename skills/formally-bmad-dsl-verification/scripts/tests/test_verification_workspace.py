import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import verification_workspace


class VerificationWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_scope(self) -> None:
        self.assertEqual(verification_workspace.slugify("DSL Verification & Audit"), "dsl-verification-audit")

    def test_create_workspace_creates_dsl_verification_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = verification_workspace.create_workspace(module_root, "Whole DSL Branch")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "checkpoint-verification.md").is_file())
            self.assertTrue((workspace / "baseline-audit.md").is_file())
            self.assertTrue((workspace / "increment-validation-audit.md").is_file())
            self.assertTrue((workspace / "rechecks.md").is_file())
            self.assertTrue((workspace / "readiness.md").is_file())
            self.assertTrue((workspace / "traceability-audit.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
