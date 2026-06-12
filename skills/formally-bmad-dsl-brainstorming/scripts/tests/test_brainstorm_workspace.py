import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import brainstorm_workspace


class BrainstormWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_topic(self) -> None:
        self.assertEqual(brainstorm_workspace.slugify("DSL Branch & Ontology"), "dsl-branch-ontology")

    def test_create_workspace_creates_delta_validation_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = brainstorm_workspace.create_workspace(module_root, "Order Flow")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "canonical-surface.md").is_file())
            self.assertTrue((workspace / "ontology-projection.md").is_file())
            self.assertTrue((workspace / "asm-model.md").is_file())
            self.assertTrue((workspace / "proposed-deltas.md").is_file())
            self.assertTrue((workspace / "increment-validation.md").is_file())
            self.assertTrue((workspace / "generated-properties.md").is_file())
            self.assertTrue((workspace / "verification-traceability.md").is_file())
            self.assertTrue((workspace / "backend-checks.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
