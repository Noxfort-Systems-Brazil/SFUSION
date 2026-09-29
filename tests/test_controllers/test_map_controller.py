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

# File: tests/test_controllers/test_map_controller.py
# Description: Tests for the MapController.

import pytest
from unittest.mock import MagicMock
from PySide6.QtCore import Qt
from src.controllers.map_controller import MapController
from src.domain.entities import MapNode, MapEdge, DataSource, AssociationType


@pytest.fixture
def map_controller_setup(qapp):
    app_state = MagicMock()
    map_renderer = MagicMock()
    info_controller = MagicMock()
    map_view = MagicMock()

    controller = MapController(
        app_state=app_state,
        map_renderer=map_renderer,
        info_controller=info_controller
    )
    controller.setup_connections(map_view)

    return {
        "controller": controller,
        "app_state": app_state,
        "map_renderer": map_renderer,
        "info_controller": info_controller,
        "map_view": map_view
    }


def test_on_node_clicked_normal_mode(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    map_renderer = setup["map_renderer"]
    info_controller = setup["info_controller"]

    app_state.is_in_association_mode.return_value = False
    node = MapNode(id="node_1", x=0, y=0)
    app_state.get_node_by_id.return_value = node
    app_state.get_sources_associated_with_element.return_value = ["dummy_source"]

    controller._on_node_clicked("node_1")

    map_renderer.clear_highlight.assert_called_once()
    map_renderer.highlight_element.assert_called_once_with("node_1", True)
    info_controller.show_for_node.assert_called_once_with(node)
    assert controller._current_selected_element_id == "node_1"


def test_on_node_clicked_association_mode(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    info_controller = setup["info_controller"]

    app_state.is_in_association_mode.return_value = True

    controller._on_node_clicked("node_1")

    app_state.associate_selected_source_to_element.assert_called_once_with("node_1")
    info_controller.show_for_node.assert_not_called()


def test_on_edge_clicked_normal_mode(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    map_renderer = setup["map_renderer"]
    info_controller = setup["info_controller"]

    app_state.is_in_association_mode.return_value = False
    edge = MapEdge(id="edge_10", from_node="a", to_node="b", shape=[(0, 0), (1, 1)])
    app_state.get_edge_by_id.return_value = edge
    app_state.get_edge_pair_id.return_value = "-edge_10"
    app_state.get_sources_associated_with_element.side_effect = lambda eid: ["source"] if eid == "edge_10" else []

    controller._on_edge_clicked("edge_10")

    map_renderer.clear_highlight.assert_called_once()
    map_renderer.highlight_element.assert_any_call("edge_10", True)
    map_renderer.highlight_element.assert_any_call("-edge_10", True)
    info_controller.show_for_edge.assert_called_once_with(edge)


def test_on_empty_space_clicked(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    info_controller = setup["info_controller"]

    controller._current_selected_element_id = "edge_10"
    controller._on_empty_space_clicked()

    assert controller._current_selected_element_id is None
    info_controller.hide_panel.assert_called_once()
    app_state.exit_association_mode.assert_called_once()


def test_on_association_mode_changed(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    map_view = setup["map_view"]

    controller._on_association_mode_changed(True)
    map_view.setCursor.assert_called_with(Qt.CrossCursor)

    controller._on_association_mode_changed(False)
    map_view.setCursor.assert_called_with(Qt.ArrowCursor)


def test_on_association_updated_for_current_selection(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    app_state = setup["app_state"]
    map_renderer = setup["map_renderer"]

    controller._current_selected_element_id = "edge_10"
    app_state.get_edge_by_id.return_value = MapEdge(id="edge_10", from_node="a", to_node="b", shape=[(0, 0), (1, 1)])
    app_state.get_edge_pair_id.return_value = "-edge_10"
    app_state.get_sources_associated_with_element.return_value = []

    controller._on_association_updated("source_path", "edge_10")

    map_renderer.clear_highlight.assert_called_once()
    map_renderer.highlight_element.assert_any_call("edge_10", False)
    map_renderer.highlight_element.assert_any_call("-edge_10", False)


def test_draw_map(map_controller_setup):
    setup = map_controller_setup
    controller = setup["controller"]
    map_renderer = setup["map_renderer"]

    controller.draw_map()
    map_renderer.draw_map.assert_called_once()
