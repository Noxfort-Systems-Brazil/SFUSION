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

# File: src/utils/cuda_loader.py
# Author: Gabriel Moraes
# Date: 2026-08-14

"""CUDA Dynamic Library Loader - Auto-discovers and preloads NVIDIA runtime libraries for CUDA bindings (llama-cpp, torch)."""

import os
import sys
import glob
import ctypes
import logging

logger = logging.getLogger(__name__)

_CUDA_LIBS_PRELOADED = False


def ensure_cuda_libs() -> bool:
    """Discovers and preloads CUDA/NVIDIA shared libraries installed in Python environments

    (e.g., nvidia-cuda-runtime-cu12, nvidia-cublas-cu12, nvidia-* packages).
    This ensures that C/C++ extensions such as llama_cpp find libcudart.so, libcublas.so, etc.
    """
    global _CUDA_LIBS_PRELOADED
    if _CUDA_LIBS_PRELOADED:
        return True

    lib_dirs = []

    # 1. Search site-packages and sys.path directories
    search_paths = list(sys.path)
    if hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix:
        search_paths.append(sys.prefix)

    for path_entry in search_paths:
        if not path_entry or not os.path.isdir(path_entry):
            continue
        # Check direct nvidia folder or site-packages/nvidia
        candidate_nvidia_dirs = []
        if os.path.basename(path_entry) == "nvidia":
            candidate_nvidia_dirs.append(path_entry)
        else:
            sub_nvidia = os.path.join(path_entry, "nvidia")
            if os.path.isdir(sub_nvidia):
                candidate_nvidia_dirs.append(sub_nvidia)

        for n_dir in candidate_nvidia_dirs:
            for root, dirs, _ in os.walk(n_dir):
                if os.path.basename(root) == "lib" and root not in lib_dirs:
                    lib_dirs.append(root)

    # 2. Add Windows DLL directories if on Windows
    if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
        for d in lib_dirs:
            try:
                os.add_dll_directory(d)
            except Exception as e:
                logger.debug(f"Failed to add DLL directory {d}: {e}")

    # 3. Update LD_LIBRARY_PATH for current process and spawned subprocesses
    if lib_dirs:
        current_ld = os.environ.get("LD_LIBRARY_PATH", "")
        existing_parts = current_ld.split(":") if current_ld else []
        new_parts = [d for d in lib_dirs if d not in existing_parts]
        if new_parts:
            updated_ld = ":".join(new_parts + ([current_ld] if current_ld else []))
            os.environ["LD_LIBRARY_PATH"] = updated_ld

    # 4. Explicitly preload shared objects with RTLD_GLOBAL on POSIX systems
    # Loading order matters for CUDA dependencies
    preload_patterns = [
        "libcudart.so*",
        "libnvrtc.so*",
        "libnvrtc-builtins.so*",
        "libcublasLt.so*",
        "libcublas.so*",
        "libcufft.so*",
        "libcurand.so*",
        "libcusolver.so*",
        "libcusparse.so*",
        "libcudnn*.so*",
    ]

    loaded_count = 0
    loaded_files = set()

    for d in lib_dirs:
        for pat in preload_patterns:
            for f in sorted(glob.glob(os.path.join(d, pat))):
                if f not in loaded_files:
                    try:
                        ctypes.CDLL(f, mode=ctypes.RTLD_GLOBAL)
                        loaded_files.add(f)
                        loaded_count += 1
                    except Exception as e:
                        logger.debug(f"Could not preload {f}: {e}")

        # Preload any other .so files in the nvidia lib directories
        for f in sorted(glob.glob(os.path.join(d, "*.so*"))):
            if f not in loaded_files:
                try:
                    ctypes.CDLL(f, mode=ctypes.RTLD_GLOBAL)
                    loaded_files.add(f)
                    loaded_count += 1
                except Exception as e:
                    logger.debug(f"Could not preload secondary lib {f}: {e}")

    _CUDA_LIBS_PRELOADED = True
    if loaded_count > 0:
        logger.debug(f"Successfully preloaded {loaded_count} CUDA libraries from {len(lib_dirs)} directories.")
    return True
