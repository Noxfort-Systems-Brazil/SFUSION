# SFUSION (Smart Fusion) is an open-source visual data engineering platform for kinematic normalization and telemetry fusion.
# SPDX-FileCopyrightText: 2026 Noxfort Systems <dev@noxfort.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
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

# File: tests/test_utils/test_slm_telemetry.py
# Author: Gabriel Moraes
# Date: October 2026

import os
import pytest
from unittest.mock import patch
from src.utils.slm_telemetry import setup_slm_logger, get_hardware_telemetry


def test_setup_slm_logger():
    logger = setup_slm_logger()
    assert logger.name == "SLM_TELEMETRY"
    assert len(logger.handlers) >= 1
    assert not logger.propagate


def test_get_hardware_telemetry_with_psutil():
    telem = get_hardware_telemetry()
    assert isinstance(telem, str)
    assert len(telem) > 0


def test_get_hardware_telemetry_nvidia_smi():
    pid = str(os.getpid())
    mock_smi_output = f"{pid}, 128.5\n"

    with patch("subprocess.check_output", return_value=mock_smi_output):
        telem = get_hardware_telemetry()
        assert "128.5" in telem or "MB" in telem or "RAM" in telem
