import tempfile
import unittest
from pathlib import Path

import import_inventory


class ImportInventoryTests(unittest.TestCase):
    def test_safe_source_id_is_stable_for_nested_paths(self):
        self.assertEqual(import_inventory.safe_source_id("docs/prd.md"), "docs__prd.md")

    def test_discover_markdown_excludes_module_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_root = root / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)
            (root / "docs").mkdir()
            (root / "docs" / "prd.md").write_text("# PRD\n", encoding="utf-8")
            (module_root / "reports").mkdir()
            (module_root / "reports" / "import-report.md").write_text("# Generated\n", encoding="utf-8")

            artifacts = import_inventory.discover_markdown(root, module_root)

            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0]["path"], "docs/prd.md")
            self.assertEqual(artifacts[0]["kind_hint"], "prd")


if __name__ == "__main__":
    unittest.main()
