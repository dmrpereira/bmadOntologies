import tempfile
import unittest
from pathlib import Path

import setup_environment


class SetupEnvironmentTests(unittest.TestCase):
    def test_ensure_structure_creates_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_root = root / "_bmad" / "formally-bmad"
            canonical = module_root / "canonical"

            setup_environment.ensure_structure(module_root, canonical)

            self.assertTrue((canonical / "model").is_dir())
            self.assertTrue((canonical / "status.md").is_file())
            self.assertTrue((module_root / "provenance" / "contradiction-override-ledger.md").is_file())
            self.assertTrue((module_root / "indexes" / "index.md").is_file())

    def test_discover_artifacts_finds_bmad_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "prd.md").write_text("# PRD\n", encoding="utf-8")

            artifacts = setup_environment.discover_artifacts(root)

            self.assertEqual(len(artifacts), 1)
            self.assertEqual(artifacts[0]["path"], "docs/prd.md")


if __name__ == "__main__":
    unittest.main()
