import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGroupBox
from ui.editor.editor_panel import EditorPanel
from src.domain.entities import DataSource, AssociationType


@pytest.fixture
def editor_panel(qapp, mock_i18n):
    panel = EditorPanel(i18n=mock_i18n)
    return panel


def test_editor_panel_initialization(editor_panel):
    assert editor_panel.isHidden()
    assert editor_panel.minimumWidth() >= 250
    assert editor_panel.sumo_id_value.isReadOnly()
    assert editor_panel.source_list_widget is not None


def test_show_data(editor_panel):
    editor_panel.show_data("Test Edge", "edge_123", "Main Avenue")
    assert editor_panel.sumo_id_value.text() == "edge_123"
    assert editor_panel.real_name_input.text() == "Main Avenue"
    group_box = editor_panel.findChild(QGroupBox)
    assert group_box is not None
    assert group_box.title() == "Test Edge"


def test_show_data_without_real_name(editor_panel):
    editor_panel.show_data("Test Node", "node_99", None)
    assert editor_panel.sumo_id_value.text() == "node_99"
    assert editor_panel.real_name_input.text() == ""


def test_update_sources_list_and_get_selected(editor_panel):
    source1 = DataSource(name="Radar 1", path="/data/radar1", association_type=AssociationType.LOCAL)
    source2 = DataSource(name="Radar 2", path="/data/radar2", association_type=AssociationType.LOCAL)
    source3 = DataSource(name="Camera 3", path="/data/camera3", association_type=AssociationType.LOCAL)

    # Initially empty
    editor_panel.update_sources_list([], set())
    assert editor_panel.source_list_widget.count() == 0

    # Populate with source1 and source3 selected
    editor_panel.update_sources_list([source1, source2, source3], {"/data/radar1", "/data/camera3"})
    assert editor_panel.source_list_widget.count() == 3

    item0 = editor_panel.source_list_widget.item(0)
    item1 = editor_panel.source_list_widget.item(1)
    item2 = editor_panel.source_list_widget.item(2)

    assert item0.text() == "Radar 1"
    assert item0.checkState() == Qt.Checked
    assert item1.text() == "Radar 2"
    assert item1.checkState() == Qt.Unchecked
    assert item2.text() == "Camera 3"
    assert item2.checkState() == Qt.Checked

    selected = editor_panel.get_selected_source_ids()
    assert set(selected) == {"/data/radar1", "/data/camera3"}


def test_save_and_close_signals(editor_panel):
    emitted_save = []
    emitted_close = []

    editor_panel.save_clicked.connect(lambda name: emitted_save.append(name))
    editor_panel.close_clicked.connect(lambda: emitted_close.append(True))

    editor_panel.real_name_input.setText("Updated Street")
    editor_panel._on_save_clicked()
    assert emitted_save == ["Updated Street"]

    editor_panel.close_button.click()
    assert emitted_close == [True]
