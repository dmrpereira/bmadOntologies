import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import architecture_workspace


class ArchitectureWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_title(self) -> None:
        self.assertEqual(architecture_workspace.slugify("DSL Architecture & Validation"), "dsl-architecture-validation")

    def test_create_workspace_creates_dsl_architecture_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = architecture_workspace.create_workspace(module_root, "Order Platform")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "architecture.md").is_file())
            self.assertTrue((workspace / "design-decisions.md").is_file())
            self.assertTrue((workspace / "architecture-deltas.md").is_file())
            self.assertTrue((workspace / "architecture-validation-status.md").is_file())
            self.assertTrue((workspace / "ontology-refinement.md").is_file())
            self.assertTrue((workspace / "asm-refinement.md").is_file())
            self.assertTrue((workspace / "verification-obligations.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
