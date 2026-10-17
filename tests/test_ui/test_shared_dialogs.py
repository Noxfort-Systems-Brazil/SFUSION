# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
# SPDX-FileCopyrightText: 2026 Noxfort Systems <dev@noxfort.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
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

# File: tests/test_ui/test_shared_dialogs.py
# Author: Gabriel Moraes
# Date: October 2026

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
