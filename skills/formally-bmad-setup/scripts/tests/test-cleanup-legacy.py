import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "cleanup-legacy.py"


class CleanupLegacyScriptTests(unittest.TestCase):
    def test_help_runs(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--help"], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout.lower())


if __name__ == "__main__":
    unittest.main()
