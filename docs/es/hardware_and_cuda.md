# 🚀 Aceleración por Hardware y Configuración CUDA

SFusion utiliza aceleración por GPU para ejecutar el modelo **Phi-4-mini** en sub-segundos sin recurrir a servicios en la nube.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 🧠 [Pipeline Neuronal](neural_pipeline.md)

---

## 1. Cargador Dinámico de Bibliotecas CUDA (`src/utils/cuda_loader.py`)

Descubre de forma automática las bibliotecas empaquetadas en paquetes pip (`nvidia-cuda-runtime-cu12`, `nvidia-cublas-cu12`) y las inyecta en memoria antes de instanciar `llama.cpp`.

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

---

## 2. Configuración en `config/slm_settings.json`

* `n_gpu_layers: -1`: 100% de capas descargadas en la GPU.
* `n_ctx: 16384`: Soporte para estructuras JSON extensas.
* `flash_attn: true`: Ahorro de memoria VRAM y mayor velocidad.
* `temperature: 0.0`: Decodificación estrictamente determinista.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Pipeline Neuronal](neural_pipeline.md)
* [Pruebas](testing.md)
