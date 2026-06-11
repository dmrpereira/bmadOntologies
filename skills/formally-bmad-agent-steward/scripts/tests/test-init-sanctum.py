import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "init-sanctum.py"
SPEC = importlib.util.spec_from_file_location("init_sanctum", SCRIPT_PATH)
init_sanctum = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(init_sanctum)


class InitSanctumTests(unittest.TestCase):
    def test_capability_discovery_skips_first_breath(self):
        with tempfile.TemporaryDirectory() as tmp:
            refs = Path(tmp)
            (refs / "first-breath.md").write_text("---\nname: First Breath\ncode: first\n---\n", encoding="utf-8")
            (refs / "cap.md").write_text(
                "---\nname: Test Capability\ncode: test-cap\ndescription: Does work.\n---\n",
                encoding="utf-8",
            )

            capabilities = init_sanctum.discover_capabilities(refs)

            self.assertEqual(len(capabilities), 1)
            self.assertEqual(capabilities[0]["code"], "test-cap")

    def test_substitute_vars_replaces_known_values(self):
        result = init_sanctum.substitute_vars("Hello {name}", {"name": "Steward"})

        self.assertEqual(result, "Hello Steward")


if __name__ == "__main__":
    unittest.main()
