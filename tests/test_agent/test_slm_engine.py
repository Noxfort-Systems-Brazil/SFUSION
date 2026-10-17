# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
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

# File: tests/test_agent/test_slm_engine.py
# Author: Gabriel Moraes
# Date: October 2026

import pytest
from unittest.mock import patch, MagicMock
from src.agent.slm_engine import SLMEngine
from src.slm.llm_provider import LLMInferenceProvider
from src.slm.prompt_builder import SchemaPromptBuilder
from src.slm.neuro_symbolic_resolver import NeuroSymbolicResolver
from src.core.schemas import KinematicMap


def test_llm_provider_init_no_llama():
    with patch('src.slm.llm_provider.Llama', None):
        provider = LLMInferenceProvider()
        assert not provider.is_available


def test_llm_provider_init_success():
    mock_llama = MagicMock()
    with patch('src.slm.llm_provider.Llama', mock_llama):
        provider = LLMInferenceProvider(model_path="dummy.gguf")
        assert provider.is_available


def test_build_prompt():
    builder = SchemaPromptBuilder()
    raw_content = '{"col1": 1, "col2": 2}'
    prompt, keys = builder.build_prompt(raw_content, "TestSource", "GLOBAL")
    assert prompt is not None
    assert "Available Columns in Dataset:" in prompt
    assert "col1" in keys and "col2" in keys


def test_neuro_symbolic_resolver():
    raw_data = {"speed_col": "jams.speedKMH"}
    available_keys = ["jams.speed", "jams.speedKMH"]
    kmap = NeuroSymbolicResolver.resolve_schema(raw_data, available_keys, "GLOBAL")
    assert kmap.speed_col == "jams.speed"
    assert kmap.flow_col is None


def test_slm_engine_orchestration_with_mock():
    mock_provider = MagicMock(spec=LLMInferenceProvider)
    mock_provider.is_available = True
    mock_provider.generate.return_value = '{"speed_col": "col1"}'

    engine = SLMEngine(provider=mock_provider)
    result = engine.discover_schema('{"col1": 1}', "Test", "GLOBAL")

    assert isinstance(result, KinematicMap)
    assert result.speed_col == "col1"
    mock_provider.generate.assert_called_once()


def test_unload():
    mock_provider = MagicMock(spec=LLMInferenceProvider)
    engine = SLMEngine(provider=mock_provider)
    engine.unload()
    mock_provider.unload.assert_called_once()


def test_slm_engine_fallback_when_llm_unavailable():
    mock_provider = MagicMock(spec=LLMInferenceProvider)
    mock_provider.is_available = False

    engine = SLMEngine(provider=mock_provider)
    result = engine.discover_schema('{"speed": 60, "flow": 120}', "TestSensor", "LOCAL")

    assert isinstance(result, KinematicMap)
    assert result.speed_col == "speed"
    assert result.flow_col == "flow"
    assert result.confidence_score == 0.85
    mock_provider.generate.assert_not_called()
