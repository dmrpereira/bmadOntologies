import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "cleanup-legacy.py"


class CleanupLegacyScriptTests(unittest.TestCase):
    def test_help_runs(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())

    def test_accepts_multiple_skills_dirs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bmad_dir = root / "_bmad"
            module_root = bmad_dir / "formally-bmad-dsl"
            module_root.mkdir(parents=True)
            legacy_skill = bmad_dir / "legacy-formally-bmad-dsl" / "example-skill"
            legacy_skill.mkdir(parents=True)
            (legacy_skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")

            (root / ".claude" / "skills").mkdir(parents=True)
            codex_skill = root / ".codex" / "skills" / "example-skill"
            codex_skill.mkdir(parents=True)

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--bmad-dir",
                    str(bmad_dir),
                    "--module-code",
                    "formally-bmad-dsl",
                    "--also-remove",
                    "legacy-formally-bmad-dsl",
                    "--skills-dir",
                    str(root / ".claude" / "skills"),
                    "--skills-dir",
                    str(root / ".codex" / "skills"),
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
            self.assertFalse((bmad_dir / "legacy-formally-bmad-dsl").exists())
            self.assertTrue(module_root.exists())


if __name__ == "__main__":
    unittest.main()
