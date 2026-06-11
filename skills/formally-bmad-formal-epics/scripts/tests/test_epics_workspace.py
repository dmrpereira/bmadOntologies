import tempfile
import unittest
from pathlib import Path

import epics_workspace


class EpicsWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_epics(self):
        self.assertEqual(epics_workspace.slugify("   "), "epics")

    def test_create_workspace_writes_epic_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)

            result = epics_workspace.create_workspace(module_root, "Release Epics")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "epics.md").is_file())
            self.assertTrue((workspace / "requirement-coverage.md").is_file())
            self.assertTrue((workspace / "story-obligations.md").is_file())


if __name__ == "__main__":
    unittest.main()
