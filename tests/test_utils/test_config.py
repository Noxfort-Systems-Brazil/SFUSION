import json
import pytest
from src.utils.config import ConfigManager


def test_config_load_nonexistent_file(tmp_path):
    fake_path = str(tmp_path / "does_not_exist.json")
    mgr = ConfigManager(fake_path)
    mgr.load_config()
    assert mgr._config_data == {}
    assert mgr.get("any_key", "default_val") == "default_val"


def test_config_load_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{ this is not valid json }")

    mgr = ConfigManager(str(bad_file))
    mgr.load_config()
    assert mgr._config_data == {}


def test_config_get_set_save(tmp_path):
    config_file = tmp_path / "subdir" / "settings.json"
    mgr = ConfigManager(str(config_file))

    mgr.set("language", "pt_BR")
    mgr.set("zoom", 2.5)

    assert mgr.get("language") == "pt_BR"
    assert mgr.get("zoom") == 2.5
    assert mgr.get("missing", 42) == 42

    mgr.save_config()
    assert config_file.exists()

    # Reload into a fresh manager
    mgr2 = ConfigManager(str(config_file))
    mgr2.load_config()
    assert mgr2.get("language") == "pt_BR"
    assert mgr2.get("zoom") == 2.5
