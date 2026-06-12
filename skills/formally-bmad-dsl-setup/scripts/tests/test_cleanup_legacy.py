import importlib.util
from pathlib import Path


TEST_PATH = Path(__file__).with_name("test-cleanup-legacy.py")
SPEC = importlib.util.spec_from_file_location("test_cleanup_legacy_hyphen", TEST_PATH)
test_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(test_module)

CleanupLegacyScriptTests = test_module.CleanupLegacyScriptTests
