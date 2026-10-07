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
