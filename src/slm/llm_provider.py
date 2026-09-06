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

# File: src/slm/llm_provider.py
# Author: Gabriel Moraes
# Date: June 2026
# Description:
#    Low-level LLM Hardware and Inference Provider.
#    Encapsulates llama.cpp runtime, GPU layer offloading, and memory cleanup.

import os
import json
import logging
import gc
from typing import Optional, List, Dict, Any
from src.utils.i18n import backend_i18n
from src.utils.cuda_loader import ensure_cuda_libs
from src.utils.slm_telemetry import slm_logger, get_hardware_telemetry

ensure_cuda_libs()

try:
    from llama_cpp import Llama
except Exception:
    Llama = None

logger = logging.getLogger(__name__)


class LLMInferenceProvider:
    """
    Manages the lifecycle and execution of local GGUF models on GPU/CPU.
    Provides clean abstraction over C++/CUDA llama.cpp library.
    """

    def __init__(self, config_path: Optional[str] = None, model_path: Optional[str] = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'slm_settings.json')

        self.config: Dict[str, Any] = {
            "model_path": "src/models/Phi-4-mini-reasoning-UD-Q6_K_XL.gguf",
            "n_gpu_layers": -1,
            "n_ctx": 16384,
            "flash_attn": True,
            "verbose": False,
            "max_tokens": 512,
            "temperature": 0.0,
            "repeat_penalty": 1.15
        }

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
                self.config.update(loaded_config)
        except Exception as e:
            logger.warning(backend_i18n.t("slm.config_load_failed", path=config_path, error=str(e)))

        self.model_path = model_path if model_path else self.config.get("model_path")
        self.llm: Optional[Any] = None
        self._initialize_model()

    def _initialize_model(self):
        """Loads GGUF weights into GPU VRAM."""
        if Llama is None:
            logger.warning(backend_i18n.t("slm.llama_not_installed"))
            return

        try:
            logger.info(backend_i18n.t("slm.loading", path=self.model_path))
            slm_logger.info("--- INIT LLM PROVIDER ---")
            slm_logger.info(f"Model Path: {self.model_path}")
            slm_logger.info(f"Config: {json.dumps(self.config)}")
            slm_logger.info(f"Hardware Before Load: {get_hardware_telemetry()}")

            self.llm = Llama(
                model_path=self.model_path,
                n_gpu_layers=self.config.get("n_gpu_layers", -1),
                n_ctx=self.config.get("n_ctx", 16384),
                flash_attn=self.config.get("flash_attn", True),
                verbose=self.config.get("verbose", False)
            )
            logger.info(backend_i18n.t("slm.loaded"))
            slm_logger.info(f"Hardware After Load: {get_hardware_telemetry()}")
        except Exception as e:
            logger.error(backend_i18n.t("slm.load_failed", error=str(e)))
            self.llm = None

    @property
    def is_available(self) -> bool:
        """Checks if LLM model is successfully loaded in memory."""
        return self.llm is not None

    def generate(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop_tokens: Optional[List[str]] = None
    ) -> str:
        """
        Executes raw LLM completion for the given prompt.
        """
        if not self.is_available:
            raise RuntimeError("LLM model is not loaded.")

        max_toks = max_tokens if max_tokens is not None else self.config.get("max_tokens", 512)
        temp = temperature if temperature is not None else self.config.get("temperature", 0.0)
        stops = stop_tokens if stop_tokens is not None else ["```", "<|end|>", "<|im_end|>", "--- END OF INSTRUCTIONS ---", "---"]
        repeat_penalty = self.config.get("repeat_penalty", 1.15)

        response = self.llm(
            prompt,
            max_tokens=max_toks,
            temperature=temp,
            repeat_penalty=repeat_penalty,
            stop=stops,
            echo=False
        )

        output_text = response["choices"][0]["text"].strip()
        return output_text

    def unload(self):
        """Releases model from GPU VRAM and triggers PyTorch cache eviction."""
        if self.llm is not None:
            del self.llm
            self.llm = None

        gc.collect()
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

        logger.info(backend_i18n.t("slm.unloaded"))
        slm_logger.info("--- MODEL UNLOADED ---")
        slm_logger.info(f"Hardware After Unload: {get_hardware_telemetry()}")
