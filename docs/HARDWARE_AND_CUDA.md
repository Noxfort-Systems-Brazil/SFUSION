# 🚀 Hardware Acceleration & CUDA Configuration

SFUSION employs a localized Small Language Model (SLM) — **Phi-4-mini-reasoning** (quantized as GGUF Q6_K_XL, ~3.5GB) — for semantic schema discovery. To deliver sub-second inference during high-volume ETL mapping, the engine leverages GPU hardware acceleration via CUDA and `llama.cpp`.

> [!NOTE]
> For details on the neuro-symbolic resolver and prompt engineering, see [[docs/NEURAL_PIPELINE]]. For overall setup, see [[README]].

---

## ⚡ CUDA Dynamic Library Loader (`src/utils/cuda_loader.py`)

Python wheels for C/C++ extensions such as `llama-cpp-python` often fail to locate CUDA runtime shared libraries (`libcudart.so`, `libcublas.so`) if CUDA is not installed globally at `/usr/local/cuda`.

To solve this friction-free, SFusion implements an automated pre-load discovery hook:

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

### How It Works:
1. Searches `sys.path` and virtual environment site-packages for bundled pip packages:
   * `nvidia-cuda-runtime-cu12`
   * `nvidia-cublas-cu12`
2. Discovers essential shared objects:
   * `libcudart.so*`
   * `libcublas.so*`
   * `libcublasLt.so*`
3. Dynamically injects the discovered directories into `LD_LIBRARY_PATH` and preloads libraries into the process address space via `ctypes.CDLL(..., mode=ctypes.RTLD_GLOBAL)`.
4. Guarantees that `llama_cpp.Llama` initializes with full TensorCore and GPU offloading enabled.

---

## ⚙️ SLM Engine Configuration (`config/slm_settings.json`)

The model hyperparameters and runtime constraints are defined in `config/slm_settings.json`:

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

| Parameter | Recommended Value | Explanation |
| :--- | :--- | :--- |
| `model_path` | `src/models/Phi-4-mini-...` | Path to the GGUF model binary. |
| `n_gpu_layers` | `-1` | Number of model layers offloaded to VRAM (`-1` offloads 100% of layers). |
| `n_ctx` | `16384` | Context window size in tokens, allowing large JSON/CSV header hierarchies. |
| `flash_attn` | `true` | Enables FlashAttention for optimized VRAM footprint and faster inference. |
| `temperature` | `0.0` | Deterministic greedy decoding to prevent hallucinations in schema routing. |
| `max_tokens` | `512` | Token generation limit sufficient for `KinematicMap` JSON output. |

---

## 🖥️ Hardware Requirements

### GPU Mode (Recommended)
* **NVIDIA GPU**: RTX 3060 / 4060 or higher (Compute Capability $\ge 7.0$).
* **VRAM**: Minimum 6 GB dedicated VRAM (8 GB+ recommended).
* **Driver**: NVIDIA Linux Driver $\ge 525.60$ (CUDA 12.x compatible).
* **Python packages**: `llama-cpp-python`, `nvidia-cuda-runtime-cu12`, `nvidia-cublas-cu12`.

### CPU Fallback Mode
If no compatible NVIDIA GPU is detected or if `llama-cpp-python` is compiled without CUDA:
* SFusion automatically falls back to CPU multi-threading.
* Requires 16 GB+ system RAM and a modern 8-core CPU.
* To force CPU mode, set `"n_gpu_layers": 0` in `config/slm_settings.json`.

---

## 📊 Telemetry & Monitoring (`src/utils/slm_telemetry.py`)

SFusion continuously logs hardware health and resource utilization to prevent VRAM memory leaks and thermal throttling.

* Reads GPU metrics via `nvidia-smi` queries: VRAM allocated, total VRAM, and GPU utilization percentage.
* Reads system metrics via `psutil`: RAM usage and CPU load.
* Outputs telemetric events to `Sfusion_slm.log` and `sfusion.log`.

---

## 🔗 Related Documentation
* [[docs/INDEX]] - Knowledge Base Map of Content
* [[ARCHITECTURE]] - System Architecture and Layer Design
* [[docs/NEURAL_PIPELINE]] - Small Language Model Integration
* [[README]] - Setup, Prerequisites, and Installation Guide
