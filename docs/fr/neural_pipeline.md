# 🧠 Pipeline Neural et Moteur SLM

Le **Pipeline Neural de SFusion** applique une architecture **Neuro-Symbolique** locale pour identifier les schémas de capteurs urbains grâce au modèle **Phi-4-mini-reasoning** sur `llama.cpp` accéléré par CUDA.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🚀 [Accélération CUDA](hardware_and_cuda.md)

---

## 1. Architecture Neuro-Symbolique

1. **Couche Neurale** : Le modèle SLM local analyse le contenu des fichiers et interprète la sémantique (`spd_kmh`, `vitesse`, `currentSpeed`).
2. **Couche Symbolique** : `NeuroSymbolicResolver` vérifie les propositions par rapport aux règles physiques du trafic et émet le schéma `KinematicMap`.

---

## 2. Composants Principaux

* **`SLMEngine`** : Façade d'orchestration de l'inférence.
* **`LLMInferenceProvider`** : Gestion de l'exécution `llama.cpp`, chargement en VRAM (`n_gpu_layers = -1`) et décodage déterministe (`temperature = 0.0`).
* **`SchemaPromptBuilder`** : Génération de chemins hiérarchiques pour les objets JSON et CSV.
* **`SLMOutputParser`** : Suppression des réflexions internes balisées par `<think>...</think>`.
* **`NeuroSymbolicResolver`** : Validation heuristique (`SPEED_CANDIDATES`, `FLOW_CANDIDATES`).

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Accélération CUDA](hardware_and_cuda.md)
* [Modèles de Données](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Sous licence AGPLv3.</small>
</div>
