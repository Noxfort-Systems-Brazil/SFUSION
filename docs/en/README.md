<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — Canonical Technical Documentation
### Architecture, Neural Schema Discovery & Vector Physics
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)

---

🌐 **Languages:** **[🇺🇸 English](README.md)** • **[🇧🇷 Português (Brasil)](../pt-br/README.md)** • **[🇪🇸 Español](../es/README.md)** • **[🇫🇷 Français](../fr/README.md)** • **[🇷🇺 Русский](../ru/README.md)** • **[🇨🇳 简体中文](../zh/README.md)** • **[📖 Central Hub](../README.md)**

---

</div>

## Welcome to the Official Technical Documentation

This directory houses the canonical, comprehensive technical documentation suite for **SFusion Mapper** (SYNAPSE Fusion) — the "Day Zero" visual data engineering and kinematic normalization tool developed by Noxfort Systems. SFusion bridges the gap between messy, heterogeneous urban mobility sensor feeds (Waze, TomTom, inductive loops, radar cameras) and strict microscopic traffic simulation environments (such as SUMO).

## Index of Specialized Guides

| Guide | Scope & Focus | Key Topics |
| :--- | :--- | :--- |
| 🏛️ **[Technical Architecture](architecture.md)** | Architectural Specification | Clean MVC, Builder pattern dependency injection, PySide6 View layer, background service delegation, and AppState reactive Single Source of Truth. |
| 📖 **[Core Concepts](core_concepts.md)** | Theoretical Foundations | "Day Zero" paradigm, SUMO network graph topology (MapNode/MapEdge), neuro-symbolic inference, and the Medallion Data Architecture (Bronze/Silver/Gold). |
| 🗃️ **[Data Models & Schemas](data_models.md)** | Schema & Entity Blueprint | Immutable domain entities, Pydantic v2 `KinematicMap` contract, temporary SQLite WAL staging tables, and final unified Apache Parquet schema. |
| ⚡ **[High-Performance ETL](etl_pipeline.md)** | Ingestion Engine | Multi-threaded `QThreadPool` orchestration, `SensorBatchProcessor`, MD5 hashing, zlib compression, and SQLite WAL PRAGMA concurrency tuning. |
| 📐 **[Vector Physics Engine](math_engine.md)** | Polars AST Compilation | Zero-GIL SIMD vector transformations, SI unit normalization ($km/h$, $m/s$, $mph$), Space Mean Speed (Harmonic Mean), and fundamental traffic density $k = q / v$. |
| 🧠 **[Neural Pipeline (SLM)](neural_pipeline.md)** | Local AI Reasoning | Embedded quantized *Phi-4-mini* GGUF, `llama.cpp` runtime, hierarchical prompt generation, `<think>` token filtering, and `NeuroSymbolicResolver`. |
| 🚀 **[Hardware Acceleration & CUDA](hardware_and_cuda.md)** | GPU Infrastructure | Dynamic CUDA shared library loader (`ensure_cuda_libs`), `slm_settings.json`, TensorCore utilization, CPU fallback, and system telemetry. |
| 🔄 **[System Workflow](system_workflow.md)** | Data Lifecycle | Deterministic 5-phase execution: Map Topology Ingestion, Sensor Registration, Association & Discovery, Staging ETL, and Columnar Parquet Export. |
| 🖥️ **[User Guide & Operations](user_guide.md)** | Operator Manual | Visual canvas navigation (pan/zoom), bidirectional edge pairing, local and global sensor association, manual schema override, and `.sfm.json` projects. |
| 🧪 **[Testing & Quality Assurance](testing.md)** | QA Standards | 66 automated Pytest unit tests, GUI decoupling, deterministic AI mocking, code coverage generation, and test suite breakdown across 8 modules. |
| ⚡ **[Internal API Reference](api_reference.md)** | Class & Signal Contracts | Technical specification of domain state, services, repository patterns, Qt Signals, and controller mediation. |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i>
</div>
