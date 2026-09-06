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

# File: tests/test_core/test_schemas.py
# Author: Gabriel Moraes
# Date: May 2026

import pytest
from src.core.schemas import KinematicMap

def test_kinematic_map_empty():
    kmap = KinematicMap()
    assert kmap.speed_col is None
    assert kmap.flow_col is None
    assert kmap.intensity_col is None
    assert kmap.distance_col is None
    assert kmap.time_col is None
    assert kmap.occupancy_col is None
    assert kmap.confidence_score is None

def test_kinematic_map_with_data():
    kmap = KinematicMap(
        speed_col="velocidade",
        flow_col="fluxo",
        confidence_score=0.95
    )
    assert kmap.speed_col == "velocidade"
    assert kmap.flow_col == "fluxo"
    assert kmap.confidence_score == 0.95
    assert kmap.intensity_col is None
