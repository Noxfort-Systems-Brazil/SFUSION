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

# File: tests/test_core/test_map_renderer.py
# Description: Tests for the MapRenderer.

import pytest
from unittest.mock import MagicMock
from src.core.map_renderer import MapRenderer
from src.domain.entities import MapNode, MapEdge
from ui.map.map_view import MapView


@pytest.fixture
def map_renderer_setup(qapp, mock_config):
    map_view = MapView()
    app_state = MagicMock()

    renderer = MapRenderer(
        map_view=map_view,
        app_state=app_state,
        config=mock_config
    )
    return {
        "renderer": renderer,
        "map_view": map_view,
        "app_state": app_state
    }


def test_draw_empty_map(map_renderer_setup):
    setup = map_renderer_setup
    renderer = setup["renderer"]
    app_state = setup["app_state"]
    scene = setup["map_view"].scene

    app_state.get_all_nodes.return_value = []
    app_state.get_all_edges.return_value = []

    renderer.draw_map()
    assert len(scene.items()) == 0


def test_draw_map_nodes_and_edges(map_renderer_setup):
    setup = map_renderer_setup
    renderer = setup["renderer"]
    app_state = setup["app_state"]
    scene = setup["map_view"].scene

    node1 = MapNode(id="n1", x=10.0, y=20.0, node_type="priority")
    node_internal = MapNode(id="n_int", x=15.0, y=25.0, node_type="internal")
    edge1 = MapEdge(id="e1", from_node="n1", to_node="n2", shape=[(0, 0), (10, 10)])
    edge_short = MapEdge(id="e_short", from_node="n1", to_node="n2", shape=[(0, 0)])

    app_state.get_all_nodes.return_value = [node1, node_internal]
    app_state.get_all_edges.return_value = [edge1, edge_short]

    renderer.draw_map()

    # edge_short has < 2 points so it's skipped
    # node_internal has internal type so it's skipped
    # 1 edge item + 1 node item in scene
    assert "n1" in renderer._drawable_items_by_id
    assert "e1" in renderer._drawable_items_by_id
    assert "n_int" not in renderer._drawable_items_by_id
    assert len(scene.items()) == 2


def test_highlight_and_clear_element(map_renderer_setup):
    setup = map_renderer_setup
    renderer = setup["renderer"]
    app_state = setup["app_state"]

    node = MapNode(id="n1", x=0.0, y=0.0)
    edge = MapEdge(id="e1", from_node="n1", to_node="n2", shape=[(0, 0), (5, 5)])

    app_state.get_all_nodes.return_value = [node]
    app_state.get_all_edges.return_value = [edge]
    renderer.draw_map()

    # Highlight node with data (associated = True)
    renderer.highlight_element("n1", is_associated=True)
    assert len(renderer._current_highlight) == 1
    assert renderer._current_highlight[0].zValue() == 3

    # Highlight edge without data (associated = False)
    renderer.highlight_element("e1", is_associated=False)
    assert len(renderer._current_highlight) == 2
    assert renderer._current_highlight[1].zValue() == 2

    # Clear highlights restores z-values and normal brushes
    renderer.clear_highlight()
    assert len(renderer._current_highlight) == 0


def test_highlight_nonexistent_or_none(map_renderer_setup):
    renderer = map_renderer_setup["renderer"]

    # None ID
    renderer.highlight_element(None, False)
    assert len(renderer._current_highlight) == 0

    # Non-existent ID
    renderer.highlight_element("ghost_id", False)
    assert len(renderer._current_highlight) == 0

    # Clear empty
    renderer.clear_highlight()
