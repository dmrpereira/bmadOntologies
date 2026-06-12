import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import epics_workspace


class EpicsWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_title(self) -> None:
        self.assertEqual(epics_workspace.slugify("DSL Epics & Validation"), "dsl-epics-validation")

    def test_create_workspace_creates_dsl_epic_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = epics_workspace.create_workspace(module_root, "Order Platform")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "epics.md").is_file())
            self.assertTrue((workspace / "requirement-coverage.md").is_file())
            self.assertTrue((workspace / "epic-coherence.md").is_file())
            self.assertTrue((workspace / "story-obligations.md").is_file())
            self.assertTrue((workspace / "accepted-delta-lineage.md").is_file())
            self.assertTrue((workspace / "validation-posture.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
