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
