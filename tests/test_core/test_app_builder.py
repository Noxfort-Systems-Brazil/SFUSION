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

# File: tests/test_core/test_app_builder.py
# Description: Tests for the AppBuilder dependency injector.

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
