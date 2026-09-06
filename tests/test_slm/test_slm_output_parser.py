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

# File: tests/test_slm/test_slm_output_parser.py
# Author: Gabriel Moraes
# Date: June 2026

import pytest
from src.slm.slm_output_parser import SLMOutputParser

def test_extract_last_json():
    text = "Some text before { 'invalid': json } { \"valid\": \"json\" } text after"
    result = SLMOutputParser.extract_last_json(text)
    assert result == {"valid": "json"}

def test_extract_last_json_none():
    assert SLMOutputParser.extract_last_json("No json here") == {}

def test_extract_thinking_with_tags():
    text = "<think>I am thinking</think>\n{\"data\": \"value\"}"
    assert SLMOutputParser.extract_thinking(text) == "I am thinking"

def test_extract_thinking_no_tags():
    text = "I am thinking about this.\n{\"data\": \"value\"}"
    assert SLMOutputParser.extract_thinking(text) == "I am thinking about this."

def test_build_schema_data():
    raw = {"valid": "123", "empty": "", "null_str": "NULL", "none_str": "None", "real_null": None}
    clean = SLMOutputParser.build_schema_data(raw)
    assert "valid" in clean
    assert "empty" not in clean
    assert "null_str" not in clean

def test_fallback_line_parse():
    text = "speed_col=v\nflow_col=NULL\nintensity_col=k"
    parsed = SLMOutputParser.fallback_line_parse(text)
    assert parsed.get("speed_col") == "v"
    assert "flow_col" not in parsed
    assert parsed.get("intensity_col") == "k"

def test_parse_full():
    text = "<think>Reasoning...</think>\n{\"speed_col\": \"v\"}"
    thinking, data = SLMOutputParser.parse(text)
    assert thinking == "Reasoning..."
    assert data == {"speed_col": "v"}

def test_parse_fallback():
    text = "<think>Reasoning...</think>\nspeed_col=v"
    thinking, data = SLMOutputParser.parse(text)
    assert thinking == "Reasoning..."
    assert data == {"speed_col": "v"}
