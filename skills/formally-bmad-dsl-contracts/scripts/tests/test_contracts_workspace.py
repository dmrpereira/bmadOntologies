import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import contracts_workspace


class ContractsWorkspaceTests(unittest.TestCase):
    def test_slugify_defaults_to_dsl_contracts(self):
        self.assertEqual(contracts_workspace.slugify("   "), "dsl-contracts")

    def test_create_workspace_writes_contract_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            module_root = Path(tmp) / "_bmad" / "formally-bmad-dsl"
            module_root.mkdir(parents=True)

            result = contracts_workspace.create_workspace(module_root, "story-1 python")
            workspace = Path(result["workspace"])

            self.assertTrue((workspace / "contract-inventory.md").is_file())
            self.assertTrue((workspace / "grounding-audit.md").is_file())
            self.assertTrue((workspace / "manifest.json").is_file())


if __name__ == "__main__":
    unittest.main()
