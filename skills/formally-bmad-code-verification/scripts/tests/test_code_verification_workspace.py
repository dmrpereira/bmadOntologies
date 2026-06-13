import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import code_verification_workspace


class CodeVerificationWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_code_verification(self):
        self.assertEqual(code_verification_workspace.slugify("   "), "code-verification")

    def test_create_workspace_writes_report_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad-dsl"
            module_root.mkdir(parents=True)

            result = code_verification_workspace.create_workspace(module_root, "rust parser crate")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "tool-runs.md").is_file())
            self.assertTrue((workspace / "readiness.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
