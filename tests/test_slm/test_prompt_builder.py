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

# File: tests/test_slm/test_prompt_builder.py
# Description: Tests for the SchemaPromptBuilder.

import json
import pytest
from src.slm.prompt_builder import SchemaPromptBuilder


def test_extract_available_keys_json():
    builder = SchemaPromptBuilder()
    json_data = '{"sensor": {"speed": 50, "location": {"lat": 10, "lon": 20}}, "count": 5}'
    keys = builder.extract_available_keys(json_data)
    assert "count" in keys
    assert "sensor" in keys
    assert "sensor.speed" in keys
    assert "sensor.location" in keys
    assert "sensor.location.lat" in keys


def test_extract_available_keys_json_list():
    builder = SchemaPromptBuilder()
    json_list = '[{"speed": 60, "flow": 10}, {"speed": 65, "density": 20}]'
    keys = builder.extract_available_keys(json_list)
    assert "speed" in keys
    assert "flow" in keys
    assert "density" in keys


def test_extract_available_keys_csv():
    builder = SchemaPromptBuilder()
    csv_data = "timestamp,vehicle_count,average_speed\n2026-01-01,100,55"
    keys = builder.extract_available_keys(csv_data)
    assert keys == ["timestamp", "vehicle_count", "average_speed"]


def test_extract_available_keys_empty():
    builder = SchemaPromptBuilder()
    assert builder.extract_available_keys("") == []


def test_build_prompt_with_custom_templates(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    discovery_file = prompts_dir / "schema_discovery.json"
    discovery_file.write_text(json.dumps({
        "schema_discovery_prompt_local": "Map local {source_name}: {available_keys_str}\n{assoc_instructions}",
        "schema_discovery_prompt_global": "Map global {source_name}: {available_keys_str}\n{assoc_instructions}"
    }))

    assoc_file = prompts_dir / "assoc_instructions.json"
    assoc_file.write_text(json.dumps({
        "LOCAL": "Focus on lane-level kinematics.",
        "GLOBAL": "Focus on macro corridor speeds."
    }))

    builder = SchemaPromptBuilder(prompts_dir=str(prompts_dir))

    # Test Local prompt
    prompt_local, keys = builder.build_prompt('{"speed": 50}', "Loop_1", assoc_type="LOCAL")
    assert "Map local Loop_1: speed" in prompt_local
    assert "Focus on lane-level kinematics." in prompt_local
    assert keys == ["speed"]

    # Test Global prompt
    prompt_global, keys = builder.build_prompt('{"jams.speed": 40}', "Waze_1", assoc_type="GLOBAL")
    assert "Map global Waze_1: jams.speed" in prompt_global
    assert "Focus on macro corridor speeds." in prompt_global


def test_build_prompt_large_content_clipping(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    discovery_file = prompts_dir / "schema_discovery.json"
    discovery_file.write_text(json.dumps({
        "schema_discovery_prompt_local": "Data: {content_str}"
    }))

    builder = SchemaPromptBuilder(prompts_dir=str(prompts_dir))
    large_payload = "x" * 60000

    prompt, _ = builder.build_prompt(large_payload, "Sensor_Large", "LOCAL")
    assert prompt is not None
    # 50,000 + "Data: " length
    assert len(prompt) <= 50010
