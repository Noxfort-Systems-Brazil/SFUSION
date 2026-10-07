import pytest
from unittest.mock import patch, MagicMock
from src.core.app_builder import AppBuilder
from ui.main_window import MainWindow


def test_app_builder_build_success(qapp):
    builder = AppBuilder()
    window = builder.build()

    assert isinstance(window, MainWindow)
    assert builder.app_state is not None
    assert builder.map_view is not None
    assert builder.editor_panel is not None
    assert builder.sources_panel is not None
    assert builder.main_controller is not None
    assert builder.map_controller is not None
    assert builder.sources_controller is not None
    assert builder.info_controller is not None
    assert builder.settings_controller is not None


def test_app_builder_missing_config_raises(qapp):
    builder = AppBuilder()
    with patch("src.utils.config.ConfigManager.get", return_value=None):
        with pytest.raises(ValueError) as excinfo:
            builder._build_utils()
        assert "Configuration 'locale_path' or 'language' not found" in str(excinfo.value)
