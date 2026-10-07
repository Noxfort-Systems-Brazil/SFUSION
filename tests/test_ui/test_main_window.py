import pytest
from unittest.mock import patch, MagicMock
from ui.main_window import MainWindow
from ui.editor.editor_panel import EditorPanel
from ui.map.map_view import MapView
from ui.sources.sources_panel import SourcesPanel


@pytest.fixture
def main_window(qapp, mock_i18n):
    window = MainWindow(i18n=mock_i18n)
    return window


def test_main_window_initialization(main_window):
    assert main_window.windowTitle() == "main_window.window_title"
    assert main_window.statusBar() is not None
    assert main_window.splitter is not None
    assert main_window.action_save is not None
    assert not main_window.action_save.isEnabled()
    assert main_window.action_save_project is not None
    assert not main_window.action_save_project.isEnabled()


def test_set_panels(main_window, mock_i18n):
    editor = EditorPanel(i18n=mock_i18n)
    map_view = MapView()
    sources = SourcesPanel(i18n=mock_i18n)

    main_window.set_editor_panel(editor)
    main_window.set_map_view(map_view)
    main_window.set_sources_panel(sources)

    assert main_window.editor_panel is editor
    assert main_window.map_view is map_view
    assert main_window.sources_panel is sources
    assert main_window.splitter.count() == 3


def test_status_and_dialog_messages(main_window):
    main_window.show_status_message("Map loaded successfully")
    assert main_window.statusBar().currentMessage() == "Map loaded successfully"

    with patch("PySide6.QtWidgets.QMessageBox.critical") as mock_crit:
        main_window.show_error_message("Error Title", "Detailed Error")
        mock_crit.assert_called_once_with(main_window, "Error Title", "Detailed Error")

    with patch("PySide6.QtWidgets.QMessageBox.information") as mock_info:
        main_window.show_info_message("Info Title", "Detailed Info")
        mock_info.assert_called_once_with(main_window, "Info Title", "Detailed Info")


def test_set_savable_state(main_window):
    main_window.set_savable_state(True)
    assert main_window.action_save.isEnabled()
    assert main_window.action_save_project.isEnabled()

    main_window.set_savable_state(False)
    assert not main_window.action_save.isEnabled()
    assert not main_window.action_save_project.isEnabled()


def test_close_event_hard_kill(main_window):
    with patch("os._exit") as mock_exit:
        mock_event = MagicMock()
        main_window.closeEvent(mock_event)
        mock_exit.assert_called_once_with(0)
