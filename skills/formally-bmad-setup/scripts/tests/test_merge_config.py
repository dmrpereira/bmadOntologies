import importlib.util
from pathlib import Path


TEST_PATH = Path(__file__).with_name("test-merge-config.py")
SPEC = importlib.util.spec_from_file_location("test_merge_config_hyphen", TEST_PATH)
test_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(test_module)

MergeConfigScriptTests = test_module.MergeConfigScriptTests
