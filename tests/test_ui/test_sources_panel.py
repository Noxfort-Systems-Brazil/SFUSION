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

# File: tests/test_ui/test_sources_panel.py
# Description: Tests for the SourcesPanel widget.

import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QListWidgetItem
from ui.sources.sources_panel import SourcesPanel
from src.domain.entities import DataSource, AssociationType


@pytest.fixture
def sources_panel(qapp, mock_i18n):
    return SourcesPanel(i18n=mock_i18n)


def test_sources_panel_initialization(sources_panel):
    assert sources_panel.sources_list_widget is not None
    assert sources_panel.radio_global is not None
    assert sources_panel.radio_local is not None
    assert sources_panel.save_button is not None
    assert not sources_panel.save_button.isEnabled()


def test_update_sources_list_and_selection(sources_panel):
    src_global = DataSource(name="Global Weather", path="/data/weather", association_type=AssociationType.GLOBAL)
    src_associated = DataSource(name="Local Loop 1", path="/data/loop1", association_type=AssociationType.LOCAL, associated_element_id="edge_1")
    src_unassociated = DataSource(name="Local Loop 2", path="/data/loop2", association_type=AssociationType.LOCAL)

    sources_panel.update_sources_list([])
    assert sources_panel.sources_list_widget.count() == 0

    sources_panel.update_sources_list([src_global, src_associated, src_unassociated])
    assert sources_panel.sources_list_widget.count() == 3

    assert "Global" in sources_panel.sources_list_widget.item(0).toolTip()
    assert "edge_1" in sources_panel.sources_list_widget.item(1).toolTip()
    assert "Não associado" in sources_panel.sources_list_widget.item(2).toolTip()

    # Select by ID
    sources_panel.set_selected_source("/data/loop1")
    selected_items = sources_panel.sources_list_widget.selectedItems()
    assert len(selected_items) == 1
    assert selected_items[0].data(Qt.UserRole) == "/data/loop1"

    # Clear selection by passing empty ID
    sources_panel.set_selected_source("")
    assert len(sources_panel.sources_list_widget.selectedItems()) == 0


def test_set_association_type(sources_panel):
    sources_panel.set_association_type("GLOBAL")
    assert sources_panel.radio_global.isChecked()
    assert not sources_panel.radio_local.isChecked()

    sources_panel.set_association_type("LOCAL")
    assert not sources_panel.radio_global.isChecked()
    assert sources_panel.radio_local.isChecked()


def test_set_savable_state(sources_panel):
    sources_panel.set_savable_state(True)
    assert sources_panel.save_button.isEnabled()

    sources_panel.set_savable_state(False)
    assert not sources_panel.save_button.isEnabled()


def test_signals_selection_and_save(sources_panel):
    emitted_selection = []
    emitted_save = []

    sources_panel.source_selection_changed.connect(lambda s: emitted_selection.append(s))
    sources_panel.save_config_requested.connect(lambda: emitted_save.append(True))

    item = QListWidgetItem("Sensor A")
    item.setData(Qt.UserRole, "/path/to/sensorA")
    sources_panel.sources_list_widget.addItem(item)

    sources_panel._on_list_selection_changed(item, None)
    assert "/path/to/sensorA" in emitted_selection

    sources_panel._on_list_selection_changed(None, item)
    assert "" in emitted_selection

    sources_panel.save_button.setEnabled(True)
    sources_panel.save_button.click()
    assert emitted_save == [True]


def test_context_menu_triggers(sources_panel):
    src = DataSource(name="Sensor A", path="/path/sensorA", association_type=AssociationType.LOCAL)
    sources_panel.update_sources_list([src])

    # Context menu on empty space (no item)
    sources_panel._on_context_menu(QPoint(100, 100))

    # Context menu on item with mocked QMenu to avoid modal loop
    with patch("ui.sources.sources_panel.QMenu") as mock_menu_cls:
        mock_menu = MagicMock()
        mock_menu_cls.return_value = mock_menu

        item = sources_panel.sources_list_widget.item(0)
        rect = sources_panel.sources_list_widget.visualItemRect(item)
        sources_panel._on_context_menu(rect.center())

        assert mock_menu.addAction.called
        assert mock_menu.exec.called
