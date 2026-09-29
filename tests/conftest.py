# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# File: tests/conftest.py
# Description: Global pytest fixtures and Qt offscreen initialization.

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
