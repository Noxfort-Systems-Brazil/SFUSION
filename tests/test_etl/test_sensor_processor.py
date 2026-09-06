# SFusion (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
# Copyright (C) 2026 Gabriel Moraes - Noxfort Systems
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# File: tests/test_etl/test_sensor_processor.py
# Author: Gabriel Moraes
# Date: June 2026

import pytest
import os
import zlib
from unittest.mock import MagicMock
from src.etl.sensor_processor import SensorBatchProcessor
from src.core.schemas import KinematicMap


def test_sensor_processor_hash_and_compression():
    content = b"sample sensor test data"
    h = SensorBatchProcessor.calculate_hash(content)
    assert len(h) == 32
    comp = SensorBatchProcessor.compress_content(content)
    assert zlib.decompress(comp) == content


def test_sensor_processor_process_file(tmp_path):
    test_file = tmp_path / "sensor_sample.json"
    test_file.write_text('{"speed": 60.0, "lat": -23.5, "lon": -51.2}', encoding="utf-8")

    mock_extractor = MagicMock()
    mock_extractor.extract.return_value = [{
        "event_timestamp": "2026-06-08 00:00:00",
        "sensor_id": "cam_01",
        "data_payload": {"speed": 60.0, "lat": -23.5, "lon": -51.2}
    }]

    mock_transformer = MagicMock()
    mock_transformer.apply_physics.return_value = [{
        "event_timestamp": "2026-06-08 00:00:00",
        "sensor_id": "cam_01",
        "data_payload": {"speed_val": 60.0, "flow_val": 1.0, "intensity_val": 0.016, "lat": -23.5, "lon": -51.2}
    }]

    processor = SensorBatchProcessor(extractor=mock_extractor, transformer=mock_transformer)
    schema = KinematicMap(speed_col="speed", confidence_score=1.0)

    raw_tuple, event_tuples = processor.process_file(
        str(test_file),
        source_name="cam_01",
        folder_schema=schema,
        assoc_type="LOCAL"
    )

    assert raw_tuple[0] == "cam_01"
    assert raw_tuple[1] == "sensor_sample.json"
    assert raw_tuple[2] == ".json"
    assert len(event_tuples) == 1
    assert event_tuples[0][1] == "cam_01"
    assert "speed_val" in event_tuples[0][2]
