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
