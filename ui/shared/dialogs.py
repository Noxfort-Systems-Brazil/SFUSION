# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
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

# File: ui/shared/dialogs.py
# Author: Gabriel Moraes
# Date: October 2026

"""Shared UI dialog helpers and utilities for SFusion Mapper."""

from PySide6.QtWidgets import QMessageBox, QWidget


def show_error_dialog(parent: QWidget, title: str, message: str) -> None:
    """Displays a standardized critical error dialog."""
    QMessageBox.critical(parent, title, message)


def show_info_dialog(parent: QWidget, title: str, message: str) -> None:
    """Displays a standardized informational dialog."""
    QMessageBox.information(parent, title, message)


def show_warning_dialog(parent: QWidget, title: str, message: str) -> None:
    """Displays a standardized warning dialog."""
    QMessageBox.warning(parent, title, message)
