# 🚀 Aceleração por Hardware e Configuração CUDA

O SFusion emprega o modelo **Phi-4-mini-reasoning** (quantizado como GGUF Q6_K_XL, ~3.5GB) para inferência semântica local. Para atingir respostas em sub-segundo, o sistema utiliza aceleração gráfica por GPU via CUDA e `llama.cpp`.

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | 🧠 [Pipeline Neural](neural_pipeline.md)

---

## 1. Carregador Dinâmico de Bibliotecas CUDA (`src/utils/cuda_loader.py`)

Pacotes Python distribuídos como wheels para extensões C/C++ frequentemente falham ao localizar bibliotecas compartilhadas de CUDA (`libcudart.so`, `libcublas.so`) quando o CUDA não está instalado globalmente no sistema operacional.

O SFusion resolve isso de forma transparente através de um hook automático de descoberta pré-inicialização:

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

### Mecanismo de Descoberta:
1. Varre `sys.path` e o diretório de site-packages do ambiente virtual em busca dos pacotes pip:
   * `nvidia-cuda-runtime-cu12`
   * `nvidia-cublas-cu12`
2. Localiza as bibliotecas compartilhadas: `libcudart.so*`, `libcublas.so*`, `libcublasLt.so*`.
3. Injeta os caminhos no `LD_LIBRARY_PATH` e pré-carrega as bibliotecas no espaço do processo via `ctypes.CDLL(..., mode=ctypes.RTLD_GLOBAL)`.
4. Garante que `llama_cpp.Llama` inicialize com suporte pleno aos TensorCores da NVIDIA.

---

## 2. Configuração do Modelo SLM (`config/slm_settings.json`)

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

* `n_gpu_layers: -1`: Descarrega 100% das camadas neurais na memória VRAM da GPU.
* `n_ctx: 16384`: Janela ampla para acomodar estruturas JSON complexas e volumosas.
* `flash_attn: true`: Ativa FlashAttention para diminuir uso de memória e acelerar inferência.
* `temperature: 0.0`: Decodificação gulosa determinística para eliminar respostas aleatórias.

---

## 3. Fallback para CPU e Telemetria

* Caso nenhuma GPU NVIDIA compatível seja detectada, o SFusion redireciona a execução automaticamente para CPU multithread.
* O módulo de telemetria (`src/utils/slm_telemetry.py`) monitora o consumo de VRAM e RAM, gravando registros contínuos em `Sfusion_slm.log`.

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Pipeline Neural](neural_pipeline.md)
* [Diretrizes de Testes](testing.md)
