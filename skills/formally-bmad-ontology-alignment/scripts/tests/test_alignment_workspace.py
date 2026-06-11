import tempfile
import unittest
from pathlib import Path

import alignment_workspace


class AlignmentWorkspaceTests(unittest.TestCase):
    def test_default_repositories_include_expected_sources(self):
        codes = {repo["code"] for repo in alignment_workspace.DEFAULT_REPOSITORIES}

        self.assertIn("bioportal", codes)
        self.assertIn("obo-foundry", codes)
        self.assertIn("wikidata", codes)

    def test_workspace_files_are_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_root = root / "_bmad" / "formally-bmad"
            module_root.mkdir(parents=True)
            registry = module_root / "artifacts" / "ontology-alignment" / "repository-registry.json"
            mappings = module_root / "artifacts" / "ontology-alignment" / "candidate-mappings.md"
            report = module_root / "reports" / "ontology-alignment-report.md"

            alignment_workspace.write_registry(registry)
            alignment_workspace.write_mapping_skeleton(mappings)
            alignment_workspace.write_report(report, "2026-05-30T00:00:00Z", registry.parent, registry)

            self.assertTrue(registry.is_file())
            self.assertTrue(mappings.is_file())
            self.assertTrue(report.is_file())


if __name__ == "__main__":
    unittest.main()
