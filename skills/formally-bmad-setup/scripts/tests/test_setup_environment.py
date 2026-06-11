import os
import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
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

    def test_baseline_validation_passes_with_smt_and_first_order(self):
        tools = {
            "smt": [{"available": True}],
            "first_order": [{"available": True}],
            "sat": [{"available": False}],
            "temporal": [{"available": False}],
            "ontology": [{"available": False}],
        }

        baseline = setup_environment.evaluate_baseline_validation(tools)

        self.assertTrue(baseline["has_smt"])
        self.assertTrue(baseline["has_first_order_or_sat"])
        self.assertTrue(baseline["baseline_satisfied"])

    def test_baseline_validation_passes_with_smt_and_sat(self):
        tools = {
            "smt": [{"available": True}],
            "first_order": [{"available": False}],
            "sat": [{"available": True}],
            "temporal": [{"available": False}],
            "ontology": [{"available": False}],
        }

        baseline = setup_environment.evaluate_baseline_validation(tools)

        self.assertTrue(baseline["has_smt"])
        self.assertTrue(baseline["has_first_order_or_sat"])
        self.assertTrue(baseline["baseline_satisfied"])

    def test_baseline_validation_blocks_with_only_smt(self):
        tools = {
            "smt": [{"available": True}],
            "first_order": [{"available": False}],
            "sat": [{"available": False}],
            "temporal": [{"available": True}],
            "ontology": [{"available": True}],
        }

        baseline = setup_environment.evaluate_baseline_validation(tools)
        guidance = setup_environment.build_guidance(baseline, available_tool_count=3, min_required_tools=1)

        self.assertTrue(baseline["has_smt"])
        self.assertFalse(baseline["has_first_order_or_sat"])
        self.assertFalse(baseline["baseline_satisfied"])
        self.assertIn("first-order or SAT solver", guidance)

    def test_baseline_validation_blocks_with_only_first_order(self):
        tools = {
            "smt": [{"available": False}],
            "first_order": [{"available": True}],
            "sat": [{"available": False}],
            "temporal": [{"available": False}],
            "ontology": [{"available": False}],
        }

        baseline = setup_environment.evaluate_baseline_validation(tools)
        guidance = setup_environment.build_guidance(baseline, available_tool_count=1, min_required_tools=1)

        self.assertFalse(baseline["has_smt"])
        self.assertTrue(baseline["has_first_order_or_sat"])
        self.assertFalse(baseline["baseline_satisfied"])
        self.assertIn("SMT solver", guidance)

    def test_baseline_validation_blocks_with_only_proof_assistants_signal(self):
        tools = {
            "smt": [{"available": False}],
            "first_order": [{"available": False}],
            "sat": [{"available": False}],
            "temporal": [{"available": False}],
            "ontology": [{"available": False}],
        }

        baseline = setup_environment.evaluate_baseline_validation(tools)
        guidance = setup_environment.build_guidance(baseline, available_tool_count=0, min_required_tools=1)

        self.assertFalse(baseline["has_smt"])
        self.assertFalse(baseline["has_first_order_or_sat"])
        self.assertFalse(baseline["baseline_satisfied"])
        self.assertIn("SMT solver", guidance)
        self.assertIn("first-order or SAT solver", guidance)

    def test_resolve_tool_search_dirs_uses_env_and_known_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            extra_dir = Path(tmp) / "extra-tools"
            known_dir = Path(tmp) / "known-tools"
            missing_dir = Path(tmp) / "missing-tools"
            extra_dir.mkdir()
            known_dir.mkdir()

            with patch.object(setup_environment, "DEFAULT_EXTRA_TOOL_DIRS", [str(known_dir)]):
                with patch.dict("os.environ", {"FORMALLY_BMAD_EXTRA_TOOL_DIRS": os.pathsep.join([str(extra_dir), str(missing_dir)])}):
                    search_dirs = setup_environment.resolve_tool_search_dirs()

            self.assertEqual(search_dirs, [str(extra_dir), str(known_dir)])

    def test_detect_tool_uses_extra_search_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            bin_dir = Path(tmp) / "bin"
            bin_dir.mkdir()
            tool_path = bin_dir / "black"
            tool_path.write_text("#!/bin/sh\nprintf 'BLACK test build\\n'\n", encoding="utf-8")
            tool_path.chmod(0o755)

            detected = setup_environment.detect_tool("black", search_path=str(bin_dir))

            self.assertTrue(detected["available"])
            self.assertEqual(detected["path"], str(tool_path))
            self.assertEqual(detected["version"], "BLACK test build")


if __name__ == "__main__":
    unittest.main()
