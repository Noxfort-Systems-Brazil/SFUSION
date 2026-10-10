import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QWidget
from ui.shared.dialogs import show_error_dialog, show_info_dialog, show_warning_dialog


def test_shared_dialogs(qapp):
    parent = QWidget()

    with patch("ui.shared.dialogs.QMessageBox.critical") as mock_crit:
        show_error_dialog(parent, "ErrTitle", "ErrMsg")
        mock_crit.assert_called_once_with(parent, "ErrTitle", "ErrMsg")

    with patch("ui.shared.dialogs.QMessageBox.information") as mock_info:
        show_info_dialog(parent, "InfoTitle", "InfoMsg")
        mock_info.assert_called_once_with(parent, "InfoTitle", "InfoMsg")

    with patch("ui.shared.dialogs.QMessageBox.warning") as mock_warn:
        show_warning_dialog(parent, "WarnTitle", "WarnMsg")
        mock_warn.assert_called_once_with(parent, "WarnTitle", "WarnMsg")
