import tempfile
import unittest
from pathlib import Path

import architecture_workspace


class ArchitectureWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_architecture(self):
        self.assertEqual(architecture_workspace.slugify("   "), "architecture")

    def test_create_workspace_writes_architecture_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)

            result = architecture_workspace.create_workspace(module_root, "System Architecture")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "architecture.md").is_file())
            self.assertTrue((workspace / "prd-alignment.md").is_file())
            self.assertTrue((workspace / "temporal-properties.md").is_file())
            self.assertTrue((workspace / "implementation-constraints.md").is_file())


if __name__ == "__main__":
    unittest.main()
