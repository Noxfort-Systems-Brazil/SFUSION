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

# File: src/agent/slm_engine.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    SLM Engine Orchestrator (Facade Pattern).
#    Coordinates Prompt Construction, Hardware Inference, Output Parsing,
#    and Neuro-Symbolic Domain Resolution adhering strictly to SOLID principles.

import time
import logging
import json
from typing import Optional
from src.core.schemas import KinematicMap
from src.slm.prompt_builder import SchemaPromptBuilder
from src.slm.llm_provider import LLMInferenceProvider
from src.slm.slm_output_parser import SLMOutputParser
from src.slm.neuro_symbolic_resolver import NeuroSymbolicResolver
from src.utils.i18n import backend_i18n
from src.utils.slm_telemetry import slm_logger, get_hardware_telemetry

logger = logging.getLogger(__name__)


class SLMEngine:
    """
    High-level Facade / Orchestrator for Small Language Model Schema Discovery.
    Delegates infrastructure, prompt engineering, parsing, and domain physics
    to dedicated specialized services (SRP & DIP).
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        provider: Optional[LLMInferenceProvider] = None,
        prompt_builder: Optional[SchemaPromptBuilder] = None,
        resolver: Optional[type[NeuroSymbolicResolver]] = None
    ):
        self.provider = provider if provider is not None else LLMInferenceProvider(model_path=model_path)
        self.prompt_builder = prompt_builder if prompt_builder is not None else SchemaPromptBuilder()
        self.resolver = resolver if resolver is not None else NeuroSymbolicResolver

    @property
    def llm(self):
        """Backward-compatibility accessor for underlying LLM instance."""
        return self.provider.llm if self.provider else None

    @property
    def is_available(self) -> bool:
        """Returns True if the underlying inference provider is loaded and ready."""
        return self.provider is not None and self.provider.is_available

    def discover_schema(
        self,
        raw_content: str,
        source_name: str,
        assoc_type: str = "LOCAL"
    ) -> Optional[KinematicMap]:
        """
        Orchestrates the end-to-end schema discovery pipeline:
          1. Prompt Construction & Key Inspection
          2. LLM Neural Inference
          3. JSON Output & Thinking Token Extraction
          4. Neuro-Symbolic Physics Validation & Disambiguation
        """
        if not self.is_available:
            logger.warning(backend_i18n.t("slm.llama_not_installed"))
            return None

        # 1. Prompt Construction
        prompt, available_keys = self.prompt_builder.build_prompt(raw_content, source_name, assoc_type)
        if not prompt:
            return None

        try:
            logger.info(backend_i18n.t("slm.inference_start", source=source_name, temp=0.0))
            slm_logger.info(f"\n--- INFERENCE START: {source_name} ---")
            slm_logger.info(f"Assoc Type: {assoc_type}")
            slm_logger.info(f"Hardware Pre-Inference: {get_hardware_telemetry()}")

            # 2. Hardware Inference
            start_t = time.time()
            output_text = self.provider.generate(prompt)
            end_t = time.time()

            # Ensure leading brace alignment
            if not output_text.startswith("{") and "{" in output_text:
                output_text = output_text[output_text.find("{"):]
            elif not output_text.startswith("{"):
                output_text = "{\n" + output_text

            slm_logger.info(f"Inference Time: {end_t - start_t:.2f}s")
            slm_logger.info(f"Hardware Post-Inference: {get_hardware_telemetry()}")
            slm_logger.info(f"Raw Output Length: {len(output_text)} chars")

            # 3. Output Parsing (SRP)
            think_content, raw_data = SLMOutputParser.parse(output_text)

            if think_content:
                logger.info(backend_i18n.t("slm.thinking_reasoning", source=source_name, content=think_content))
                slm_logger.debug(f"Thinking Block:\n{think_content}")
            else:
                slm_logger.info("Direct JSON output generated.")

            # 4. Neuro-Symbolic Domain Physics Resolution
            kinematic_map = self.resolver.resolve_schema(
                raw_schema_data=raw_data,
                available_keys=available_keys,
                assoc_type=assoc_type
            )

            logger.info(backend_i18n.t("slm.extracted_schema", source=source_name, content=json.dumps(kinematic_map.model_dump(), indent=2)))
            slm_logger.info(f"Extracted KinematicMap:\n{json.dumps(kinematic_map.model_dump(), indent=2)}")
            slm_logger.info(f"--- INFERENCE END: {source_name} ---")

            return kinematic_map

        except Exception as e:
            logger.error(backend_i18n.t("slm.inference_failed", error=str(e)))
            return None

    def unload(self):
        """Delegates memory and VRAM release to the LLM provider."""
        if self.provider:
            self.provider.unload()
