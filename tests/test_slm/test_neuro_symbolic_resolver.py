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

# File: tests/test_slm/test_neuro_symbolic_resolver.py
# Description: Exhaustive tests for NeuroSymbolicResolver unit inference and schema resolution.

import pytest
from src.slm.neuro_symbolic_resolver import NeuroSymbolicResolver
from src.core.schemas import KinematicMap


def test_infer_speed_unit():
    # From raw_unit
    assert NeuroSymbolicResolver.infer_speed_unit(None, "mph") == "mph"
    assert NeuroSymbolicResolver.infer_speed_unit(None, "m/s") == "m/s"
    assert NeuroSymbolicResolver.infer_speed_unit(None, "mps") == "m/s"
    assert NeuroSymbolicResolver.infer_speed_unit(None, "km/h") == "km/h"

    # From column name
    assert NeuroSymbolicResolver.infer_speed_unit("speed_mph", None) == "mph"
    assert NeuroSymbolicResolver.infer_speed_unit("speed_mps", None) == "m/s"
    assert NeuroSymbolicResolver.infer_speed_unit("vel_kmh", None) == "km/h"
    assert NeuroSymbolicResolver.infer_speed_unit("speed_km_h", None) == "km/h"
    assert NeuroSymbolicResolver.infer_speed_unit("plain_speed", None) == "km/h"


def test_infer_occupancy_unit():
    # From raw unit
    assert NeuroSymbolicResolver.infer_occupancy_unit(None, "milliseconds") == "ms"
    assert NeuroSymbolicResolver.infer_occupancy_unit(None, "%") == "pct"
    assert NeuroSymbolicResolver.infer_occupancy_unit(None, "seconds") == "s"

    # From column name
    assert NeuroSymbolicResolver.infer_occupancy_unit("occupancy_ms", None) == "ms"
    assert NeuroSymbolicResolver.infer_occupancy_unit("occupancy_pct", None) == "pct"
    assert NeuroSymbolicResolver.infer_occupancy_unit("occupancy_sec", None) == "s"
    assert NeuroSymbolicResolver.infer_occupancy_unit(None, None) is None


def test_infer_distance_unit():
    assert NeuroSymbolicResolver.infer_distance_unit(None, "miles") == "miles"
    assert NeuroSymbolicResolver.infer_distance_unit(None, "km") == "km"
    assert NeuroSymbolicResolver.infer_distance_unit(None, "meters") == "m"

    assert NeuroSymbolicResolver.infer_distance_unit("dist_mile", None) == "miles"
    assert NeuroSymbolicResolver.infer_distance_unit("dist_kilometer", None) == "km"
    assert NeuroSymbolicResolver.infer_distance_unit("length_m", None) == "m"
    assert NeuroSymbolicResolver.infer_distance_unit(None, None) is None


def test_infer_time_unit():
    assert NeuroSymbolicResolver.infer_time_unit(None, "ms") == "ms"
    assert NeuroSymbolicResolver.infer_time_unit(None, "hours") == "hours"
    assert NeuroSymbolicResolver.infer_time_unit(None, "min") == "min"
    assert NeuroSymbolicResolver.infer_time_unit(None, "sec") == "s"

    assert NeuroSymbolicResolver.infer_time_unit("interval_millis", None) == "ms"
    assert NeuroSymbolicResolver.infer_time_unit("interval_h", None) == "hours"
    assert NeuroSymbolicResolver.infer_time_unit("duration_min", None) == "min"
    assert NeuroSymbolicResolver.infer_time_unit("time_s", None) == "s"
    assert NeuroSymbolicResolver.infer_time_unit(None, None) is None


def test_resolve_schema_local_with_intensity_candidate():
    raw_schema = {}
    available_keys = [
        "data.speed_kmh",
        "data.vehicle_count",
        "data.density"
    ]

    res = NeuroSymbolicResolver.resolve_schema(raw_schema, available_keys, assoc_type="LOCAL")
    assert isinstance(res, KinematicMap)
    assert res.speed_col == "data.speed_kmh"
    assert res.flow_col == "data.vehicle_count"
    assert res.intensity_col == "data.density"
    assert res.occupancy_col is None
    assert res.speed_unit == "km/h"


def test_resolve_schema_local_with_occupancy_candidate():
    raw_schema = {}
    available_keys = [
        "data.speed_kmh",
        "data.vehicle_count",
        "data.occupancy_pct"
    ]

    res = NeuroSymbolicResolver.resolve_schema(raw_schema, available_keys, assoc_type="LOCAL")
    assert isinstance(res, KinematicMap)
    assert res.speed_col == "data.speed_kmh"
    assert res.flow_col == "data.vehicle_count"
    assert res.intensity_col is None
    assert res.occupancy_col == "data.occupancy_pct"
    assert res.occupancy_unit == "pct"


def test_resolve_schema_global_clears_flow_intensity():
    raw_schema = {
        "speed_col": "jams.speed",
        "flow_col": "volume",
        "intensity_col": "density"
    }
    available_keys = ["jams.speed", "volume", "density"]

    res = NeuroSymbolicResolver.resolve_schema(raw_schema, available_keys, assoc_type="GLOBAL")
    assert res.speed_col == "jams.speed"
    assert res.flow_col is None
    assert res.intensity_col is None
