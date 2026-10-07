import os
import sys

# Ensure offscreen rendering for Qt widgets in CI/headless environments
os.environ["QT_QPA_PLATFORM"] = "offscreen"

import pytest
from unittest.mock import MagicMock
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Initializes a shared QApplication instance for widget testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app


@pytest.fixture
def mock_i18n():
    """Returns a mock I18nManager that returns key or formatted key."""
    i18n = MagicMock()
    i18n.language = "pt_BR"
    i18n.locale_dir = "locale"
    i18n.t.side_effect = lambda key, **kwargs: (
        key if not kwargs else f"{key}_{'_'.join(f'{k}={v}' for k, v in kwargs.items())}"
    )
    return i18n


@pytest.fixture
def mock_config():
    """Returns a mock ConfigManager with realistic default keys."""
    config = MagicMock()
    data = {
        "language": "pt_BR",
        "map_zoom": {"min": 0.1, "max": 10.0},
        "map_colors": {
            "edge": "#4A4A4A",
            "node": "#E74C3C",
            "highlight": "#00FF00"
        }
    }
    config.get.side_effect = lambda key, default=None: data.get(key, default)
    config._config_data = data
    return config
