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

# File: tests/test_services/test_math_engine.py
# Author: Gabriel Moraes
# Date: May 2026

import pytest
import polars as pl
from src.services.math_engine import MathEngine
from src.core.schemas import KinematicMap


def test_compile_ast_direct():
    schema = KinematicMap(speed_col="v", flow_col="q", intensity_col="k", confidence_score=1.0)
    exprs = MathEngine.compile_ast(schema)
    assert len(exprs) == 3
    aliases = [e.meta.output_name() for e in exprs]
    assert "speed_val" in aliases
    assert "flow_val" in aliases
    assert "intensity_val" in aliases


def test_compile_ast_derived():
    schema = KinematicMap(distance_col="dist", time_col="t", occupancy_col="occ", confidence_score=1.0)
    exprs = MathEngine.compile_ast(schema)
    assert len(exprs) == 3
    aliases = [e.meta.output_name() for e in exprs]
    assert "speed_val" in aliases
    assert "flow_val" in aliases
    assert "intensity_val" in aliases


def test_compile_ast_speed_units_ms_to_kmh():
    schema = KinematicMap(speed_col="speed_mps", speed_unit="m/s", confidence_score=1.0)
    exprs = MathEngine.compile_ast(schema)
    df = pl.DataFrame({"speed_mps": [10.0, 20.0]})
    res = df.with_columns(exprs).select("speed_val").to_series().to_list()
    assert res == [36.0, 72.0]


def test_compile_ast_speed_units_mph_to_kmh():
    schema = KinematicMap(speed_col="speed_mph", speed_unit="mph", confidence_score=1.0)
    exprs = MathEngine.compile_ast(schema)
    df = pl.DataFrame({"speed_mph": [60.0]})
    res = df.with_columns(exprs).select("speed_val").to_series().to_list()
    assert pytest.approx(res[0], 0.01) == 96.56


def test_compile_ast_derived_units():
    # 1000 meters in 36 seconds = 100 km/h
    schema = KinematicMap(distance_col="d", distance_unit="m", time_col="t", time_unit="s", confidence_score=1.0)
    exprs = MathEngine.compile_ast(schema)
    df = pl.DataFrame({"d": [1000.0], "t": [36.0]})
    res = df.with_columns(exprs).select("speed_val").to_series().to_list()
    assert pytest.approx(res[0], 0.01) == 100.0


def test_compile_aggregations():
    cols = ["speed_val", "flow_val", "intensity_val", "event_timestamp", "sensor_lat", "sensor_lon"]
    agg_exprs = MathEngine.compile_aggregations(cols)
    assert len(agg_exprs) >= 3
    aliases = [e.meta.output_name() for e in agg_exprs]
    assert "speed_val" in aliases
    assert "flow_val" in aliases
    assert "intensity_val" in aliases
    assert "event_timestamp" in aliases
    assert "lat" in aliases
    assert "lon" in aliases


def test_compile_aggregations_minimal():
    cols = ["speed_val"]
    agg_exprs = MathEngine.compile_aggregations(cols)
    assert len(agg_exprs) == 2
    aliases = [e.meta.output_name() for e in agg_exprs]
    assert "speed_val" in aliases
