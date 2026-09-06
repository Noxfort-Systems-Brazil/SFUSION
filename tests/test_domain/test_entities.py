# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Gabriel Moraes - Noxfort Systems
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

# File: tests/test_domain/test_entities.py
# Author: Gabriel Moraes
# Date: November 2025

import pytest
from src.domain.entities import DataSource, AssociationType, MapNode, MapEdge

def test_datasource_default_initialization():
    ds = DataSource(path="/tmp/data.csv", name="Data")
    assert ds.path == "/tmp/data.csv"
    assert ds.name == "Data"
    assert ds.file_types == []
    assert ds.id.startswith("src_")
    assert ds.parser_id is None
    assert ds.association_type == AssociationType.UNASSOCIATED
    assert ds.associated_element_id is None

def test_datasource_custom_initialization():
    ds = DataSource(
        path="/tmp/test.json",
        name="Test Source",
        file_types=["JSON"],
        parser_id="json_parser",
        association_type=AssociationType.GLOBAL
    )
    assert ds.file_types == ["JSON"]
    assert ds.parser_id == "json_parser"
    assert ds.association_type == AssociationType.GLOBAL

def test_mapnode_initialization():
    node = MapNode(id="node_1", x=10.5, y=20.5)
    assert node.id == "node_1"
    assert node.x == 10.5
    assert node.y == 20.5
    assert node.node_type == "unknown"
    assert node.real_name is None

def test_mapedge_initialization():
    edge = MapEdge(id="edge_1", from_node="node_1", to_node="node_2")
    assert edge.id == "edge_1"
    assert edge.from_node == "node_1"
    assert edge.to_node == "node_2"
    assert edge.shape == []
    assert edge.real_name is None
