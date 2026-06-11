import tempfile
import unittest
from pathlib import Path

import brainstorm_workspace


class BrainstormWorkspaceTests(unittest.TestCase):
    def test_slugify_returns_stable_slug(self):
        self.assertEqual(brainstorm_workspace.slugify("Formal Specs & Ontologies"), "formal-specs-ontologies")

    def test_create_workspace_writes_starter_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)

            result = brainstorm_workspace.create_workspace(module_root, "Test Topic")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "brainstorm.md").is_file())
            self.assertTrue((workspace / "candidate-delta.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
