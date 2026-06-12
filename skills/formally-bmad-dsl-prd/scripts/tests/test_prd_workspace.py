import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import prd_workspace


class PrdWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_title(self) -> None:
        self.assertEqual(prd_workspace.slugify("DSL PRD & Validation"), "dsl-prd-validation")

    def test_create_workspace_creates_dsl_prd_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = prd_workspace.create_workspace(module_root, "Order Platform")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "prd.md").is_file())
            self.assertTrue((workspace / "requirements.md").is_file())
            self.assertTrue((workspace / "accepted-deltas.md").is_file())
            self.assertTrue((workspace / "validation-status.md").is_file())
            self.assertTrue((workspace / "verification-obligations.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
