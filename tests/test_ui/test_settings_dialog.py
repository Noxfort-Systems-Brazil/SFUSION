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

# File: tests/test_ui/test_settings_dialog.py
# Description: Tests for the SettingsDialog.

import pytest
from ui.settings.settings_dialog import SettingsDialog


def test_settings_dialog_initialization(qapp, mock_i18n, mock_config):
    dialog = SettingsDialog(i18n=mock_i18n, config=mock_config)

    assert dialog.language_combo is not None
    assert dialog.language_combo.count() == 6
    assert dialog.get_selected_language() == "pt_BR"


def test_settings_dialog_change_language(qapp, mock_i18n, mock_config):
    dialog = SettingsDialog(i18n=mock_i18n, config=mock_config)

    idx_en = dialog.language_combo.findData("en")
    assert idx_en != -1
    dialog.language_combo.setCurrentIndex(idx_en)

    assert dialog.get_selected_language() == "en"


def test_settings_dialog_custom_initial_config(qapp, mock_i18n, mock_config):
    mock_config.get.side_effect = lambda k, d=None: "es" if k == "language" else d
    dialog = SettingsDialog(i18n=mock_i18n, config=mock_config)

    assert dialog.get_selected_language() == "es"
