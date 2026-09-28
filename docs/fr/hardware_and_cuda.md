# 🚀 Accélération Matérielle et Configuration CUDA

SFusion utilise l'accélération GPU pour exécuter localement le modèle **Phi-4-mini** avec un temps de réponse inférieur à la seconde.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🧠 [Pipeline Neural](neural_pipeline.md)

---

## 1. Chargeur Dynamique de Bibliothèques CUDA (`src/utils/cuda_loader.py`)

Recherche automatiquement les bibliothèques CUDA distribuées via pip (`nvidia-cuda-runtime-cu12`, `nvidia-cublas-cu12`) et les précharge en mémoire avant l'initialisation de `llama.cpp`.

```python
from src.utils.cuda_loader import ensure_cuda_libs
ensure_cuda_libs()
```

---

## 2. Configuration dans `config/slm_settings.json`

* `n_gpu_layers: -1` : Transfert de 100% des couches du modèle sur la VRAM de la carte graphique.
* `n_ctx: 16384` : Prise en charge des schémas JSON étendus.
* `flash_attn: true` : Diminution de l'empreinte mémoire et accélération du traitement.
* `temperature: 0.0` : Décodage déterministe prévenant les réponses aléatoires.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Pipeline Neural](neural_pipeline.md)
* [Tests](testing.md)
