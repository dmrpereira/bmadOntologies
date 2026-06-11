import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "merge-config.py"


class MergeConfigScriptTests(unittest.TestCase):
    def test_declares_pyyaml_dependency_and_argparse(self):
        content = SCRIPT.read_text(encoding="utf-8")

        self.assertIn('dependencies = ["pyyaml"]', content)
        self.assertIn("argparse.ArgumentParser", content)
        self.assertIn("--config-path", content)


if __name__ == "__main__":
    unittest.main()
