# 🧠 Pipeline Neuronal y Motor SLM

El **Pipeline Neuronal de SFusion** implementa una arquitectura **Neuro-Simbólica** local para el mapeo inteligente de telemetría urbana mediante el modelo **Phi-4-mini-reasoning** sobre `llama.cpp` con aceleración CUDA.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 🚀 [Aceleración CUDA](hardware_and_cuda.md)

---

## 1. Arquitectura Neuro-Simbólica

1. **Capa Neuronal**: El SLM local interpreta nombres arbitrarios de columnas (`spd_kmh`, `velocidad`, `currentSpeed`).
2. **Capa Simbólica**: `NeuroSymbolicResolver` valida las sugerencias contra heurísticas de tráfico e infiere unidades de medida, emitiendo el blueprint `KinematicMap`.

---

## 2. Componentes Principales

* **`SLMEngine`**: Fachada de orquestación de IA.
* **`LLMInferenceProvider`**: Runtime de `llama.cpp` con descarga a VRAM (`n_gpu_layers = -1`) y decodificación determinista (`temperature = 0.0`).
* **`SchemaPromptBuilder`**: Generador de rutas jerárquicas pontuadas en esquemas JSON y CSV.
* **`SLMOutputParser`**: Filtro de etiquetas de razonamiento interno `<think>...</think>`.
* **`NeuroSymbolicResolver`**: Validador contra diccionarios heurísticos (`SPEED_CANDIDATES`, `FLOW_CANDIDATES`, etc.).

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Aceleración CUDA](hardware_and_cuda.md)
* [Modelos de Datos](data_models.md)
