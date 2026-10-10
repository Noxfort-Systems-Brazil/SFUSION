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
