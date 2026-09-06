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

# File: src/slm/prompt_builder.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    Specialized Prompt Builder for SLM Schema Discovery.
#    Handles key inspection, schema template loading, and prompt interpolation.

import os
import json
import logging
from typing import List, Optional, Tuple
from src.utils.i18n import backend_i18n

logger = logging.getLogger(__name__)


class SchemaPromptBuilder:
    """
    Constructs contextual prompts for Local and Global traffic sensor schema mapping.
    Inspects heterogeneous JSON and CSV structures to extract dotted key hierarchies.
    """

    def __init__(self, prompts_dir: Optional[str] = None):
        if prompts_dir is None:
            self.prompts_dir = os.path.join(os.path.dirname(__file__), '..', 'prompts')
        else:
            self.prompts_dir = prompts_dir

    def extract_available_keys(self, content_str: str) -> List[str]:
        """
        Extracts flattened dotted property paths from JSON objects or lists,
        or column headers from CSV data.
        """
        try:
            parsed_data = json.loads(content_str)

            def get_keys(d, prefix=''):
                keys = set()
                if isinstance(d, dict):
                    for k, v in d.items():
                        full_key = f"{prefix}.{k}" if prefix else k
                        keys.add(full_key)
                        keys.update(get_keys(v, full_key))
                elif isinstance(d, list):
                    for item in d[:5]:
                        keys.update(get_keys(item, prefix))
                return list(keys)

            if isinstance(parsed_data, list):
                available_keys = set()
                for item in parsed_data[:5]:
                    available_keys.update(get_keys(item))
                return sorted(list(available_keys))
            else:
                return sorted(list(set(get_keys(parsed_data))))
        except Exception:
            # Fallback for CSV or plain text column lists
            first_line = content_str.split('\n')[0].strip()
            if ',' in first_line:
                return [c.strip() for c in first_line.split(',') if c.strip()]
            return []

    def load_prompt_templates(self) -> dict:
        """Loads prompt templates from schema_discovery.json."""
        prompt_path = os.path.join(self.prompts_dir, 'schema_discovery.json')
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(backend_i18n.t("slm.prompt_load_failed", path=prompt_path, error=str(e)))
            return {}

    def load_association_instructions(self, assoc_type: str, source_name: str) -> str:
        """Loads sensor association instructions from assoc_instructions.json."""
        assoc_path = os.path.join(self.prompts_dir, 'assoc_instructions.json')
        try:
            with open(assoc_path, 'r', encoding='utf-8') as f:
                assoc_templates = json.load(f)
        except Exception as e:
            logger.warning(backend_i18n.t("slm.assoc_load_failed", path=assoc_path, error=str(e)))
            assoc_templates = {}

        assoc_key = assoc_type.upper()
        assoc_template = assoc_templates.get(
            assoc_key,
            f"This sensor ({source_name}) is {assoc_key}. Search for all applicable traffic variables."
        )
        return assoc_template.replace("{source_name}", source_name)

    def build_prompt(self, raw_content: str, source_name: str, assoc_type: str = "LOCAL") -> Tuple[Optional[str], List[str]]:
        """
        Builds the complete prompt string ready for SLM inference.
        Returns a tuple of (formatted_prompt_str, available_keys_list).
        """
        try:
            content_str = raw_content.decode('utf-8', errors='ignore') if isinstance(raw_content, bytes) else str(raw_content)
        except Exception:
            content_str = str(raw_content)

        available_keys = self.extract_available_keys(content_str)
        available_keys_str = ", ".join(available_keys)

        # Context clipping to avoid GPU context overflow
        if len(content_str) > 50000:
            logger.warning(backend_i18n.t("slm.file_too_large", size=len(content_str)))
            content_str = content_str[:50000]

        prompts = self.load_prompt_templates()
        prompt_key = 'schema_discovery_prompt_global' if assoc_type.upper() == 'GLOBAL' else 'schema_discovery_prompt_local'
        prompt_template = prompts.get(prompt_key, '')
        if isinstance(prompt_template, list):
            prompt_template = '\n'.join(prompt_template)

        if not prompt_template:
            return None, available_keys

        assoc_instructions = self.load_association_instructions(assoc_type, source_name)

        formatted_prompt = (
            prompt_template
            .replace("{source_name}", source_name)
            .replace("{content_str}", content_str)
            .replace("{available_keys_str}", available_keys_str)
            .replace("{assoc_type}", assoc_type)
            .replace("{assoc_instructions}", assoc_instructions)
        )

        return formatted_prompt, available_keys
