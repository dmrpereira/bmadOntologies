import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contract_stubs_workspace


class ContractStubsWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_dsl_contract_stubs(self):
        self.assertEqual(contract_stubs_workspace.slugify("   "), "dsl-contract-stubs")

    def test_create_workspace_writes_stub_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad-dsl"
            module_root.mkdir(parents=True)

            result = contract_stubs_workspace.create_workspace(module_root, "story-1 rust")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "stubs.md").is_file())
            self.assertTrue((workspace / "scaffold-plan.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
