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

# File: tests/test_services/test_extractors.py
# Author: Gabriel Moraes
# Date: November 2025

import pytest
from src.services.extractors import UniversalExtractor
from datetime import datetime

def test_extract_json():
    ext = UniversalExtractor()
    content = b'[{"speed": 50, "time": 1600000000000}]'
    res = ext.extract("test.json", content, "sensor1")
    assert len(res) == 1
    assert res[0]["sensor_id"] == "sensor1"
    assert "event_timestamp" in res[0]
    assert res[0]["data_payload"]["speed"] == 50

def test_extract_json_dict():
    ext = UniversalExtractor()
    content = b'{"alerts": [{"speed": 50}]}'
    res = ext.extract("test.json", content, "sensor1")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == 50

def test_extract_csv():
    ext = UniversalExtractor()
    content = b'speed,time\n50,160000'
    res = ext.extract("test.csv", content, "sensor2")
    assert len(res) == 1
    assert res[0]["data_payload"]["speed"] == "50"
    
def test_extract_invalid():
    ext = UniversalExtractor()
    # CSV reader might still process it as a single empty column row, so we just ensure it doesn't crash
    content = b'\x00\x01\x02'
    res = ext.extract("test.bin", content)
    assert isinstance(res, list)
