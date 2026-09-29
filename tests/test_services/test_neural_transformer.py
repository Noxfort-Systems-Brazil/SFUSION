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

# File: tests/test_services/test_neural_transformer.py
# Description: Tests for the NeuralTransformer service.

import pytest
from unittest.mock import patch, MagicMock
from src.services.neural_transformer import NeuralTransformer
from src.core.schemas import KinematicMap


@pytest.fixture
def neural_transformer():
    return NeuralTransformer()


def test_initialize_and_cleanup_encoder(neural_transformer):
    with patch("src.services.neural_transformer.SLMEngine") as mock_engine_cls:
        mock_engine = MagicMock()
        mock_engine_cls.return_value = mock_engine

        neural_transformer.initialize_encoder()
        assert neural_transformer.slm_engine is mock_engine

        # Idempotent
        neural_transformer.initialize_encoder()
        assert mock_engine_cls.call_count == 1

        neural_transformer.cleanup_encoder()
        assert neural_transformer.slm_engine is None
        mock_engine.unload.assert_called_once()


def test_discover_schema_flow_and_cache(neural_transformer):
    schema = KinematicMap(
        speed_col="velocity",
        flow_col="NULL",
        intensity_col="density",
        speed_unit="km/h"
    )

    mock_engine = MagicMock()
    mock_engine.discover_schema.return_value = schema
    neural_transformer.slm_engine = mock_engine

    # 1. First discovery (calls engine, filters "NULL" to None)
    res1 = neural_transformer.discover_schema("sample text", "sensor_loop_1", assoc_type="LOCAL")
    assert res1 is schema
    assert res1.flow_col is None  # Cleaned up from "NULL"
    mock_engine.discover_schema.assert_called_once_with("sample text", "sensor_loop_1", "LOCAL")

    # 2. Second discovery for the same sensor (cache hit)
    res2 = neural_transformer.discover_schema("sample text", "sensor_loop_1", assoc_type="LOCAL")
    assert res2 is schema
    assert mock_engine.discover_schema.call_count == 1  # Not called again


def test_discover_schema_when_engine_not_initialized(neural_transformer):
    neural_transformer.slm_engine = None
    res = neural_transformer.discover_schema("raw text", "sensor_x")
    assert res is None


def test_apply_physics_empty_events(neural_transformer):
    result = neural_transformer.apply_physics([], None)
    assert result == []


def test_apply_physics_with_schema_local(neural_transformer):
    events = [
        {
            "event_timestamp": "2026-06-01T12:00:00Z",
            "sensor_id": "loop_sensor_42",
            "data_payload": {
                "velocity": 60.0,
                "volume": 15,
                "density": 22.5,
                "lat": -23.55,
                "lon": -46.63
            }
        },
        {
            "event_timestamp": "2026-06-01T12:01:00Z",
            "sensor_id": "loop_sensor_42",
            "data_payload": {
                "velocity": 40.0,
                "volume": 25,
                "density": 35.0,
                "lat": -23.55,
                "lon": -46.63
            }
        }
    ]

    schema = KinematicMap(
        speed_col="velocity",
        flow_col="volume",
        intensity_col="density",
        speed_unit="km/h"
    )

    output = neural_transformer.apply_physics(events, schema, assoc_type="LOCAL")
    assert len(output) == 1
    record = output[0]
    assert record["sensor_id"] == "loop_sensor_42"
    payload = record["data_payload"]

    # Speed harmonic mean (40 & 60 -> 48 km/h)
    assert payload["speed_val"] == pytest.approx(48.0, rel=1e-2)
    # Flow sum (15 + 25 = 40)
    assert payload["flow_val"] == 40.0
    # Intensity mean ((22.5 + 35.0) / 2 = 28.75)
    assert payload["intensity_val"] == pytest.approx(28.75, rel=1e-2)
    assert payload["lat"] == -23.55
    assert payload["lon"] == -46.63


def test_apply_physics_global_sensor(neural_transformer):
    events = [
        {
            "event_timestamp": "2026-06-01T10:00:00Z",
            "sensor_id": "waze_segment_1",
            "data_payload": {
                "jams": {"speed": 50.0},
                "lat": 0.0,
                "lon": 0.0
            }
        }
    ]

    schema = KinematicMap(
        speed_col="jams.speed",
        flow_col="vehicles",
        intensity_col="level",
        speed_unit="km/h"
    )

    output = neural_transformer.apply_physics(events, schema, assoc_type="GLOBAL")
    assert len(output) == 1
    payload = output[0]["data_payload"]

    assert payload["speed_val"] == 50.0
    assert payload["flow_val"] == 0.0
    assert payload["intensity_val"] == 0.0


def test_apply_physics_without_schema(neural_transformer):
    events = [
        {
            "event_timestamp": "2026-06-01T10:00:00Z",
            "sensor_id": "unknown_sensor",
            "data_payload": {
                "val": 100
            }
        }
    ]

    output = neural_transformer.apply_physics(events, schema=None)
    assert len(output) == 1
    payload = output[0]["data_payload"]
    assert payload["speed_val"] is None
    assert payload["flow_val"] is None
    assert payload["intensity_val"] is None

