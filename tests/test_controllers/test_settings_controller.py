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
