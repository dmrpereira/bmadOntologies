import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import stories_workspace


class StoriesWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_story_id(self) -> None:
        self.assertEqual(stories_workspace.slugify("DSL Story & Validation"), "dsl-story-validation")

    def test_create_workspace_creates_dsl_story_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            module_root = Path(tmpdir)
            result = stories_workspace.create_workspace(module_root, "Story 1.1")

            workspace = Path(result["workspace"])
            self.assertTrue((workspace / "story.md").is_file())
            self.assertTrue((workspace / "acceptance-criteria.md").is_file())
            self.assertTrue((workspace / "formalization.md").is_file())
            self.assertTrue((workspace / "alignment.md").is_file())
            self.assertTrue((workspace / "blockers.md").is_file())
            self.assertTrue((workspace / "readiness.md").is_file())
            self.assertTrue((workspace / "delta-lineage.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
