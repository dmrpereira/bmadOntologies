import tempfile
import unittest
from pathlib import Path

import prd_workspace


class PrdWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_prd(self):
        self.assertEqual(prd_workspace.slugify("   "), "prd")

    def test_create_workspace_writes_prd_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)

            result = prd_workspace.create_workspace(module_root, "My Product")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "prd.md").is_file())
            self.assertTrue((workspace / "requirements.md").is_file())
            self.assertTrue((workspace / "verification-obligations.md").is_file())


if __name__ == "__main__":
    unittest.main()
