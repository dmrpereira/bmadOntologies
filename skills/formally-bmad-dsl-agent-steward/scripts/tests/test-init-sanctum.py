import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
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

    def test_main_creates_capabilities_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "project"
            skill_root = Path(tmp) / "skill"
            bmad_dir = project_root / "_bmad"
            assets_dir = skill_root / "assets"
            refs_dir = skill_root / "references"

            assets_dir.mkdir(parents=True)
            refs_dir.mkdir(parents=True)
            bmad_dir.mkdir(parents=True)

            (assets_dir / "INDEX-template.md").write_text("# Index\n- `CAPABILITIES.md`\n", encoding="utf-8")
            (assets_dir / "PERSONA-template.md").write_text("# Persona\n", encoding="utf-8")
            (assets_dir / "CREED-template.md").write_text("# Creed\n", encoding="utf-8")
            (assets_dir / "BOND-template.md").write_text("# Bond\n", encoding="utf-8")
            (assets_dir / "MEMORY-template.md").write_text("# Memory\n", encoding="utf-8")
            (assets_dir / "CAPABILITIES-template.md").write_text(
                "# Capabilities\n\n{capabilities-table}\n",
                encoding="utf-8",
            )

            (refs_dir / "first-breath.md").write_text("# First Breath\n", encoding="utf-8")
            (refs_dir / "accept-canonical-delta.md").write_text(
                "---\nname: Accept Canonical Delta\ncode: accept-delta\ndescription: Promote accepted deltas.\n---\n",
                encoding="utf-8",
            )

            argv = sys.argv
            try:
                sys.argv = [
                    str(SCRIPT_PATH),
                    str(project_root),
                    str(skill_root),
                ]
                with redirect_stdout(io.StringIO()):
                    exit_code = init_sanctum.main()
            finally:
                sys.argv = argv

            self.assertEqual(exit_code, 0)
            sanctum_dir = project_root / "_bmad" / "memory" / init_sanctum.SANCTUM_DIR
            capabilities = sanctum_dir / "CAPABILITIES.md"
            self.assertTrue(capabilities.exists())
            self.assertIn("accept-delta", capabilities.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
