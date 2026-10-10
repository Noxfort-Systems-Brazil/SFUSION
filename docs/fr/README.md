<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — Suite de Documentation Technique
### Architecture Système, Découverte Neurale de Schémas et Physique Vectorielle
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Actif-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)

---

🌐 **Langues :** **[🇺🇸 English](../en/README.md)** • **[🇧🇷 Português (Brasil)](../pt-br/README.md)** • **[🇪🇸 Español](../es/README.md)** • **[🇫🇷 Français](README.md)** • **[🇷🇺 Русский](../ru/README.md)** • **[🇨🇳 简体中文](../zh/README.md)** • **[📖 Hub Central](../README.md)**

---

</div>

## Bienvenue sur la Documentation Technique Officielle

Ce répertoire rassemble la suite complète de documentation technique en **Français** pour **SFusion Mapper** (SYNAPSE Fusion) — l'outil visuel d'ingénierie des données « Jour Zéro » et de normalisation cinématique développé par Noxfort Systems. SFusion fait le pont entre des flux de capteurs urbains hétérogènes (Waze, TomTom, boucles électromagnétiques, radars) et les environnements stricts de simulation microscopique du trafic (tels que SUMO).

## Index des Guides Spécialisés

| Guide | Portée & Domaine | Thématiques Clés |
| :--- | :--- | :--- |
| 🏛️ **[Architecture Système](architecture.md)** | Spécification Technique | Modèle MVC épuré, injection de dépendances via le pattern Builder, couche View PySide6, services d'arrière-plan et AppState réactif comme Source Unique de Vérité. |
| 📖 **[Concepts Fondamentaux](core_concepts.md)** | Fondements Théoriques | Paradigme « Jour Zéro », topologie en graphe SUMO (MapNode/MapEdge), inférence neuro-symbolique et architecture Médaillon (Bronze/Argent/Or). |
| 🗃️ **[Modèles de Données et Schémas](data_models.md)** | Dictionnaire de Données | Entités de domaine immuables, contrat Pydantic v2 `KinematicMap`, tables temporaires SQLite WAL et schéma unifié final en Apache Parquet. |
| ⚡ **[Pipeline ETL Haute Performance](etl_pipeline.md)** | Moteur d'Ingestion | Orchestration multithread via `QThreadPool`, `SensorBatchProcessor`, hachage MD5, compression zlib et configuration PRAGMA pour SQLite WAL. |
| 📐 **[Moteur de Physique Vectorielle](math_engine.md)** | Compilation AST Polars | Transformations vectorielles SIMD sans verrou GIL, normalisation SI ($km/h$, $m/s$, $mph$), vitesse moyenne spatiale harmonique et densité $k = q / v$. |
| 🧠 **[Pipeline Neural (SLM)](neural_pipeline.md)** | Raisonnement IA Local | Modèle quantifié local *Phi-4-mini* GGUF, runtime `llama.cpp`, génération de prompts hiérarchiques, filtrage des balises `<think>` et `NeuroSymbolicResolver`. |
| 🚀 **[Accélération Matérielle et CUDA](hardware_and_cuda.md)** | Infrastructure GPU | Chargeur dynamique de bibliothèques CUDA (`ensure_cuda_libs`), `slm_settings.json`, utilisation des TensorCores, repli CPU et télémétrie. |
| 🔄 **[Flux de Travail du Système](system_workflow.md)** | Cycle de Vie des Données | Exécution déterministe en 5 phases : Ingestion de Réseau, Enregistrement des Capteurs, Association et Découverte, Staging ETL et Export Parquet. |
| 🖥️ **[Guide d'Utilisation et Opérations](user_guide.md)** | Manuel Opérateur | Navigation visuelle (pan/zoom), appariement bidirectionnel des voies, association locale et globale, surcharge manuelle et projets `.sfm.json`. |
| 🧪 **[Tests et Assurance Qualité](testing.md)** | Standards de QA | 169 tests automatisés Pytest, couverture >91% backend et frontend, exécution headless Qt, mocks d'IA déterministes et découpage en 10 modules. |
| ⚡ **[Référence de l'API Interne](api_reference.md)** | Contrats de Classes et Signaux | Spécification technique des modèles de domaine, services d'arrière-plan, pattern DAO/Repository, signaux Qt et médiateurs de contrôleurs. |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i>
</div>
