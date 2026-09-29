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

# File: tests/test_controllers/test_info_controller.py
# Description: Tests for the InfoController.

import pytest
from unittest.mock import MagicMock
from src.controllers.info_controller import InfoController
from src.domain.entities import MapNode, MapEdge, DataSource, AssociationType


@pytest.fixture
def info_controller_setup(qapp, mock_i18n):
    app_state = MagicMock()
    view = MagicMock()
    map_renderer = MagicMock()

    controller = InfoController(
        app_state=app_state,
        view=view,
        map_renderer=map_renderer,
        i18n=mock_i18n
    )
    return {
        "controller": controller,
        "app_state": app_state,
        "view": view,
        "map_renderer": map_renderer,
        "i18n": mock_i18n
    }


def test_setup_connections(info_controller_setup):
    controller = info_controller_setup["controller"]
    view = info_controller_setup["view"]

    controller.setup_connections()
    view.save_clicked.connect.assert_called_once_with(controller._on_save)
    view.close_clicked.connect.assert_called_once_with(controller.hide_panel)


def test_show_for_node(info_controller_setup):
    controller = info_controller_setup["controller"]
    view = info_controller_setup["view"]
    app_state = info_controller_setup["app_state"]

    node = MapNode(id="node_1", x=10.0, y=20.0, real_name="Crossing A")
    dummy_source = DataSource(name="Cam 1", path="/cam1", association_type=AssociationType.LOCAL)

    app_state.get_available_local_sources.return_value = [dummy_source]
    app_state.get_sources_associated_with_element.return_value = [dummy_source]

    controller.show_for_node(node)

    assert controller._current_element is node
    view.update_sources_list.assert_called_once_with([dummy_source], {"/cam1"})
    view.show_data.assert_called_once_with(
        title="info_panel.title_node",
        sumo_id="node_1",
        real_name="Crossing A"
    )
    view.show.assert_called_once()
    view.raise_.assert_called_once()


def test_show_for_edge(info_controller_setup):
    controller = info_controller_setup["controller"]
    view = info_controller_setup["view"]
    app_state = info_controller_setup["app_state"]

    edge = MapEdge(id="edge_1", from_node="n1", to_node="n2", shape=[(0, 0), (10, 10)], real_name="Highway 1")
    app_state.get_available_local_sources.return_value = []
    app_state.get_sources_associated_with_element.return_value = []

    controller.show_for_edge(edge)

    assert controller._current_element is edge
    view.show_data.assert_called_once_with(
        title="info_panel.title_edge",
        sumo_id="edge_1",
        real_name="Highway 1"
    )
    view.show.assert_called_once()


def test_on_save_for_edge_with_pair(info_controller_setup):
    controller = info_controller_setup["controller"]
    view = info_controller_setup["view"]
    app_state = info_controller_setup["app_state"]
    map_renderer = info_controller_setup["map_renderer"]

    edge = MapEdge(id="edge_42", from_node="n1", to_node="n2", shape=[(0, 0), (1, 1)])
    controller._current_element = edge

    app_state.get_edge_pair_id.return_value = "-edge_42"
    view.get_selected_source_ids.return_value = ["/src/loop1", "/src/loop2"]

    controller._on_save("Avenida Brasil")

    # Name updated for both edge and its pair
    app_state.update_element_real_name.assert_any_call("edge_42", "Avenida Brasil")
    app_state.update_element_real_name.assert_any_call("-edge_42", "Avenida Brasil")

    # Associations set only for clicked edge
    app_state.set_element_associations.assert_called_once_with("edge_42", ["/src/loop1", "/src/loop2"])

    # Panel hidden and highlight cleared
    assert controller._current_element is None
    view.hide.assert_called_once()
    map_renderer.clear_highlight.assert_called_once()


def test_on_save_without_selection(info_controller_setup):
    controller = info_controller_setup["controller"]
    app_state = info_controller_setup["app_state"]

    controller._current_element = None
    controller._on_save("Some Name")
    app_state.update_element_real_name.assert_not_called()


def test_hide_panel(info_controller_setup):
    controller = info_controller_setup["controller"]
    view = info_controller_setup["view"]
    map_renderer = info_controller_setup["map_renderer"]

    controller._current_element = MapNode(id="n1", x=0, y=0)
    controller.hide_panel()

    assert controller._current_element is None
    view.hide.assert_called_once()
    map_renderer.clear_highlight.assert_called_once()
