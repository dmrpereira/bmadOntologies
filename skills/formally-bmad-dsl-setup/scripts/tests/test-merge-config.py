import unittest
from pathlib import Path
import importlib.util
import sys
import types


SCRIPT = Path(__file__).resolve().parents[1] / "merge-config.py"
SPEC = importlib.util.spec_from_file_location("dsl_merge_config", SCRIPT)
merge_config = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
yaml_stub = types.ModuleType("yaml")
yaml_stub.safe_load = lambda text: {}
yaml_stub.dump = lambda *args, **kwargs: None
sys.modules.setdefault("yaml", yaml_stub)
SPEC.loader.exec_module(merge_config)


class MergeConfigScriptTests(unittest.TestCase):
    def test_declares_pyyaml_dependency_and_argparse(self):
        content = SCRIPT.read_text(encoding="utf-8")

        self.assertIn('dependencies = ["pyyaml"]', content)
        self.assertIn("argparse.ArgumentParser", content)
        self.assertIn("--config-path", content)

    def test_variable_definitions_reads_variables_list(self):
        module_yaml = {
            "code": "formally-bmad-dsl",
            "variables": [
                {"key": "formally_bmad_dsl_project_root", "user_setting": True},
                {"key": "formally_bmad_dsl_report_format", "user_setting": True},
            ],
        }

        definitions = merge_config.variable_definitions(module_yaml)

        self.assertIn("formally_bmad_dsl_project_root", definitions)
        self.assertIn("formally_bmad_dsl_report_format", definitions)

    def test_extract_user_settings_uses_variables_list(self):
        module_yaml = {
            "variables": [
                {"key": "formally_bmad_dsl_project_root", "user_setting": True},
                {"key": "ignored", "user_setting": False},
            ]
        }
        answers = {
            "core": {"user_name": "David"},
            "module": {
                "formally_bmad_dsl_project_root": "{project-root}/_bmad/formally-bmad-dsl",
                "ignored": "x",
            },
        }

        extracted = merge_config.extract_user_settings(module_yaml, answers)

        self.assertEqual(extracted["user_name"], "David")
        self.assertIn("formally_bmad_dsl_project_root", extracted)
        self.assertNotIn("ignored", extracted)


if __name__ == "__main__":
    unittest.main()
