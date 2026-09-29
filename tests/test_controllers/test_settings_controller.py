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

# File: tests/test_controllers/test_settings_controller.py
# Description: Tests for the SettingsController.

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QDialog
from src.controllers.settings_controller import SettingsController


@pytest.fixture
def settings_controller_setup(qapp, mock_i18n, mock_config):
    main_window = MagicMock()
    controller = SettingsController(
        main_window=main_window,
        config=mock_config,
        i18n=mock_i18n
    )
    return {
        "controller": controller,
        "main_window": main_window,
        "config": mock_config,
        "i18n": mock_i18n
    }


def test_show_settings_dialog_accepted_with_language_change(settings_controller_setup):
    setup = settings_controller_setup
    controller = setup["controller"]
    config = setup["config"]
    main_window = setup["main_window"]

    config.get.side_effect = lambda k, d=None: "pt_BR" if k == "language" else d

    with patch("src.controllers.settings_controller.SettingsDialog") as mock_dialog_cls:
        dialog_mock = MagicMock()
        dialog_mock.exec.return_value = QDialog.Accepted
        dialog_mock.get_selected_language.return_value = "en"
        mock_dialog_cls.return_value = dialog_mock

        controller.show_settings_dialog()

        config.set.assert_called_once_with("language", "en")
        config.save_config.assert_called_once()
        main_window.show_info_message.assert_called_once()


def test_show_settings_dialog_accepted_without_change(settings_controller_setup):
    setup = settings_controller_setup
    controller = setup["controller"]
    config = setup["config"]
    main_window = setup["main_window"]

    config.get.side_effect = lambda k, d=None: "pt_BR" if k == "language" else d

    with patch("src.controllers.settings_controller.SettingsDialog") as mock_dialog_cls:
        dialog_mock = MagicMock()
        dialog_mock.exec.return_value = QDialog.Accepted
        dialog_mock.get_selected_language.return_value = "pt_BR"
        mock_dialog_cls.return_value = dialog_mock

        controller.show_settings_dialog()

        config.set.assert_not_called()
        config.save_config.assert_called_once()
        main_window.show_info_message.assert_not_called()


def test_show_settings_dialog_rejected(settings_controller_setup):
    setup = settings_controller_setup
    controller = setup["controller"]
    config = setup["config"]

    with patch("src.controllers.settings_controller.SettingsDialog") as mock_dialog_cls:
        dialog_mock = MagicMock()
        dialog_mock.exec.return_value = QDialog.Rejected
        mock_dialog_cls.return_value = dialog_mock

        controller.show_settings_dialog()

        config.set.assert_not_called()
        config.save_config.assert_not_called()
