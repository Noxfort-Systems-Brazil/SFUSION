# SFUSION (SYNAPSE Fusion) Mapper - "Day Zero" ETL Configuration Tool
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

# File: src/slm/slm_output_parser.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    Robust output parser for SLM inference results.
#    Extracts structured JSON schema maps and thinking content from raw LLM output,
#    regardless of whether the model emits proper <think>...</think> tags or chat markdown.

import json
import re
import logging
from typing import Dict, Optional, Tuple, List
from src.utils.i18n import backend_i18n

logger = logging.getLogger(__name__)


class SLMOutputParser:
    """
    Stateless parser that separates SLM raw output into two components:
      1. Thinking content (reasoning text for logging/debugging)
      2. Schema data (the JSON kinematic mapping and units)

    Handles edge cases like unclosed braces, Markdown fences, extra brackets,
    and missing tags by scanning for valid balanced schema JSON objects.
    """

    SCHEMA_KEYS = {
        "speed_col", "flow_col", "intensity_col", "distance_col", "time_col", "occupancy_col",
        "speed_unit", "occupancy_unit", "distance_unit", "time_unit"
    }

    @classmethod
    def extract_json_candidates(cls, text: str) -> List[dict]:
        """Finds all balanced JSON objects in text and returns valid dicts."""
        candidates = []
        for start_idx in range(len(text)):
            if text[start_idx] == '{':
                depth = 0
                for end_idx in range(start_idx, len(text)):
                    if text[end_idx] == '{':
                        depth += 1
                    elif text[end_idx] == '}':
                        depth -= 1
                        if depth == 0:
                            substr = text[start_idx:end_idx + 1]
                            try:
                                parsed = json.loads(substr)
                                if isinstance(parsed, dict):
                                    candidates.append(parsed)
                            except json.JSONDecodeError:
                                pass
                            break
        return candidates

    @classmethod
    def extract_last_json(cls, text: str) -> dict:
        """
        Finds the best matching JSON schema dictionary in the text.
        Prioritizes objects that contain canonical schema keys.
        """
        candidates = cls.extract_json_candidates(text)
        schema_candidates = [
            c for c in candidates if any(k in cls.SCHEMA_KEYS for k in c.keys())
        ]
        if schema_candidates:
            return schema_candidates[-1]
        return candidates[-1] if candidates else {}

    @classmethod
    def extract_thinking(cls, text: str) -> str:
        """
        Extracts thinking/reasoning text from the model output.
        """
        think_match = re.search(r'<think>(.*?)</think>', text, flags=re.DOTALL)
        if think_match:
            return think_match.group(1).strip()

        # Clean out JSON objects and markdown fences to isolate thinking
        cleaned = re.sub(r'\{[^{}]*\}', '', text, flags=re.DOTALL)
        cleaned = re.sub(r'```[a-zA-Z]*', '', cleaned)
        cleaned = re.sub(r'</?think>', '', cleaned)
        return cleaned.strip()

    @classmethod
    def build_schema_data(cls, parsed_json: dict) -> Dict[str, str]:
        """
        Filters the parsed JSON into a clean schema dictionary,
        discarding null/none/empty values and normalizing strings.
        """
        data = {}
        for k, v in parsed_json.items():
            k_clean = str(k).strip().strip('"\'')
            if v is not None and str(v).strip().upper() not in ["NULL", "NONE", ""]:
                data[k_clean] = str(v).strip().strip('"\'')
        return data

    @classmethod
    def fallback_regex_parse(cls, text: str) -> Dict[str, str]:
        """
        Fallback parser using regular expressions for KEY=VALUE or KEY: VALUE format.
        Used when raw JSON extraction is malformed.
        """
        data = {}
        for key in cls.SCHEMA_KEYS:
            pattern = rf'["\']?{key}["\']?\s*[:=]\s*["\']?([^"\'\s,}}\n]+)["\']?'
            match = re.search(pattern, text)
            if match:
                val = match.group(1).strip().strip('",\'')
                if val.upper() not in ["NULL", "NONE", ""]:
                    data[key] = val
        return data

    # Backward compatibility alias
    fallback_line_parse = fallback_regex_parse

    @classmethod
    def parse(cls, raw_output: str) -> Tuple[str, Dict[str, str]]:
        """
        Main entry point. Parses raw SLM output into (thinking_content, schema_data).
        """
        thinking = cls.extract_thinking(raw_output)
        parsed_json = cls.extract_last_json(raw_output)
        data = cls.build_schema_data(parsed_json) if parsed_json else {}

        # Fallback to regex line parsing if JSON did not yield valid schema keys
        if not data or not any(k in data for k in cls.SCHEMA_KEYS):
            fallback_data = cls.fallback_regex_parse(raw_output)
            if fallback_data:
                data = fallback_data

        return thinking, data
