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

# File: tests/test_utils/test_cuda_loader.py
# Author: Gabriel Moraes
# Date: 2026-08-14

import os
import sys
from unittest.mock import patch
from src.utils.cuda_loader import ensure_cuda_libs

def test_ensure_cuda_libs_returns_true():
    assert ensure_cuda_libs() is True

def test_ensure_cuda_libs_idempotent():
    # Should be fast and return True on repeated calls
    assert ensure_cuda_libs() is True
    assert ensure_cuda_libs() is True
