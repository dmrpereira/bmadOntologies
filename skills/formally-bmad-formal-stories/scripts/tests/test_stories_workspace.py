import tempfile
import unittest
from pathlib import Path

import stories_workspace


class StoriesWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_story(self):
        self.assertEqual(stories_workspace.slugify("   "), "story")

    def test_create_workspace_writes_story_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)

            result = stories_workspace.create_workspace(module_root, "Story 1.1")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "story.md").is_file())
            self.assertTrue((workspace / "acceptance-criteria.md").is_file())
            self.assertTrue((workspace / "readiness.md").is_file())
            self.assertTrue((workspace / "blockers.md").is_file())


if __name__ == "__main__":
    unittest.main()
