# 🚀 Hardware Acceleration & CUDA Configuration

SFusion employs a localized Small Language Model (SLM) — **Phi-4-mini-reasoning** (quantized as GGUF Q6_K_XL, ~3.5GB) — for semantic schema discovery. To deliver sub-second inference during high-volume ETL mapping, the engine leverages GPU hardware acceleration via CUDA and `llama.cpp`.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | 🧠 [Neural Pipeline](neural_pipeline.md)

---

## 1. CUDA Dynamic Library Loader (`src/utils/cuda_loader.py`)

Python wheels for C/C++ extensions such as `llama-cpp-python` often fail to locate CUDA runtime shared libraries (`libcudart.so`, `libcublas.so`) if CUDA is not installed globally in `/usr/local/cuda`.

To solve this friction-free, SFusion implements an automated pre-load discovery hook:

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

### Discovery & Preload Mechanism:
1. Searches `sys.path` and virtual environment site-packages for bundled pip packages:
   * `nvidia-cuda-runtime-cu12`
   * `nvidia-cublas-cu12`
2. Discovers essential shared objects: `libcudart.so*`, `libcublas.so*`, `libcublasLt.so*`.
3. Injects discovered directories into `LD_LIBRARY_PATH` and preloads libraries into the process address space via `ctypes.CDLL(..., mode=ctypes.RTLD_GLOBAL)`.
4. Guarantees that `llama_cpp.Llama` initializes with full TensorCore and GPU offloading enabled.

---

## 2. SLM Engine Configuration (`config/slm_settings.json`)

```json
{
  "model_path": "src/models/Phi-4-mini-reasoning-UD-Q6_K_XL.gguf",
  "n_gpu_layers": -1,
  "n_ctx": 16384,
  "flash_attn": true,
  "verbose": false,
  "max_tokens": 512,
  "temperature": 0.0
}
```

* `n_gpu_layers: -1`: Offloads 100% of layers to dedicated GPU VRAM.
* `n_ctx: 16384`: Accommodates large nested JSON sensor schemas.
* `flash_attn: true`: Optimizes memory bandwidth and minimizes VRAM spikes.
* `temperature: 0.0`: Deterministic greedy decoding.

---

## 3. CPU Fallback & Resource Monitoring

* If no compatible NVIDIA GPU is present, SFusion falls back smoothly to multi-threaded CPU execution.
* Telemetry tracker (`src/utils/slm_telemetry.py`) monitors GPU utilization and system RAM, logging to `Sfusion_slm.log`.

---

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [Neural Pipeline](neural_pipeline.md)
* [Testing Guide](testing.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under AGPLv3.</small>
</div>
