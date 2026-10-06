---
tags: [home, index, sfusion, hub]
aliases: [Documentation Index, Overview, Portal]
---

# 🌐 SFusion Mapper Documentation Hub

Welcome to the technical documentation library for **SFusion Mapper** (SYNAPSE Fusion) — the "Day Zero" visual data engineering and kinematic normalization tool for urban traffic simulation and AI ecosystems.

Designed to operate seamlessly on **GitHub**, as an **[Obsidian](https://obsidian.md/) Knowledge Vault**, and rendered with **Material for MkDocs**, this documentation suite covers our clean MVC architecture, local SLM neural inference, Polars vector physics, and columnar Parquet compilation.

---

## 🗺️ Master Navigation & Modules

| Subsystem / Dimension | Focus Area | Direct Link |
| :--- | :--- | :---: |
| 📚 **Master Map of Content** | Primary Obsidian Hub & Codebase Directory Map | [Explore Hub](SFUSION_MOC.md) |
| 🌐 **Multi-Language Hub** | Select documentation in 6 international languages | [Language Selector](README.md) |
| 🏛️ **System Architecture** | Clean MVC, Builder Pattern, Service Layer & Concurrency | [View Blueprint](ARCHITECTURE.md) |
| 📖 **Core Concepts** | "Day Zero" Paradigm, SUMO Graph & Medallion Architecture | [View Concepts](CORE_CONCEPTS.md) |
| 🗃️ **Data Models & Schemas** | Domain Entities, KinematicMap Blueprint & Parquet Specs | [View Schemas](DATA_MODELS.md) |
| ⚡ **High-Performance ETL** | Multi-threaded Sensor Ingestion & SQLite WAL Staging | [View ETL](ETL_PIPELINE.md) |
| 📐 **Vector Physics Engine** | Polars AST Compilation, SI Units & Harmonic Mean Speed | [View Math Engine](MATH_ENGINE.md) |
| 🧠 **Neural Pipeline (SLM)** | Phi-4-mini reasoning model, llama.cpp & Neuro-Symbolic Resolver | [View Neural](NEURAL_PIPELINE.md) |
| 🚀 **Hardware & CUDA** | GPU VRAM Offload, Dynamic Library Loader & Telemetry | [View Hardware](HARDWARE_AND_CUDA.md) |
| 🔄 **System Workflow** | 5-Phase End-to-End Data Lifecycle | [View Workflow](SYSTEM_WORKFLOW.md) |
| 🖥️ **User Guide & Operations** | Step-by-Step Interactive GUI Manual | [View User Guide](USER_GUIDE.md) |
| 🛠️ **Developer Guides** | Developer Setup, Extensibility & Architecture Rules | [View Developer Guides](DEVELOPER_GUIDES.md) |
| 📦 **Deployment & Packaging** | Standalone Executables, Docker Builds & Desktop Integration | [View Deployment](DEPLOYMENT_AND_PACKAGING.md) |
| 🧪 **Testing & QA** | 160 Pytest Automated Tests (>91% Coverage), Headless Qt & Mocks | [View Testing](TESTING.md) |
| ⚡ **API Reference** | Core Classes, Qt Signals, Methods & Contracts | [View API](API_REFERENCE.md) |

---

## ⚡ High-Level Architecture Summary

```text
       ┌────────────────────────────────────────────────────────┐
       │             SFusion Mapper Application                 │
       │     (PySide6 / Qt6 + Clean MVC Architecture)           │
       └──────────────────────────┬─────────────────────────────┘
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────────┐
│   MapView    │          │  SLM Engine  │          │    ETL Engine    │
│(QGraphicsScn)│ ◄──────► │ (Phi-4-mini) │ ◄──────► │ (QThreadPool/WAL)│
└──────┬───────┘          └──────┬───────┘          └────────┬─────────┘
       │                         │                           │
       ▼                         ▼                           ▼
┌──────────────┐          ┌──────────────┐          ┌──────────────────┐
│  AppState    │          │Neuro-Symbolic│          │  ParquetService  │
│ (SSOT/Signal)│          │  Resolver    │          │  (Snappy Gold)   │
└──────────────┘          └──────────────┘          └──────────────────┘
```

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
