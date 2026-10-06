---
tags: [moc, hub, docs, obsidian, sfusion, index]
aliases: [SFUSION MOC, Master Documentation Hub, Documentation Index, Knowledge Vault]
---

# 📚 SFusion Technical Master Documentation Hub

Welcome to the **SFusion Mapper** (SYNAPSE Fusion) technical documentation library. Designed as a high-performance, open-source Graphical User Interface and data engineering application for smart mobility ecosystems, SFusion bridges microscopic SUMO traffic networks, arbitrary sensor streams, local neuro-symbolic SLM reasoning, and vectorized Polars compilation.

This master documentation index provides deep technical coverage for core developers, simulation engineers, traffic data scientists, and systems integrators. It is fully compatible with both **GitHub** and **[Obsidian](https://obsidian.md/)**.

---

## 🗺️ Codebase Map & Directory Hierarchy

```text
SFUSION/
├── sfusion.py                  # Master Entrypoint (AppBuilder, SingleInstance, GUI Loop)
├── ARCHITECTURE.md             # Clean MVC Blueprint, Builder Pattern & Service Layer
├── pyproject.toml              # Build toolchain & project metadata
├── requirements.txt            # Python runtime dependencies
├── sfusion.spec                # PyInstaller standalone bundling specification
├── Dockerfile                  # Multi-stage Linux build container
├── docker-compose.yml          # Container composition definition
├── sync.sh                     # 1-click Git update & synchronization script
├── run.sh                      # 1-click virtual environment runner
│
├── config/                     # Configuration Systems
│   └── default_settings.json   # Base application hyperparameters
│
├── locale/                     # Frontend UI Translations (PySide6)
│   ├── en_us.json              # English (US)
│   ├── pt_br.json              # Português do Brasil
│   ├── es_es.json              # Español
│   ├── fr_fr.json              # Français
│   ├── ru_ru.json              # Русский
│   └── zh_cn.json              # 简体中文
│
├── locale_backend/             # Background Worker & Telemetry Translations
│   ├── en_us.json              # English (US)
│   ├── pt_br.json              # Português do Brasil
│   ├── es_es.json              # Español
│   ├── fr_fr.json              # Français
│   ├── ru_ru.json              # Русский
│   └── zh_cn.json              # 简体中文
│
├── docs/                       # Comprehensive Knowledge Vault
│   ├── SFUSION_MOC.md          # Master Documentation Hub (This File)
│   ├── index.md                # MkDocs Entry Point & Portal
│   ├── README.md               # Multi-Language Documentation Hub
│   ├── ARCHITECTURE.md         # Technical Architecture & Patterns
│   ├── CORE_CONCEPTS.md        # Day Zero Paradigm, SUMO Graphs & Medallion Design
│   ├── DATA_MODELS.md          # Domain Entities, KinematicMap Schemas & Parquet Specs
│   ├── ETL_PIPELINE.md         # High-Performance Ingestion Engine & SQLite WAL Staging
│   ├── MATH_ENGINE.md          # Vector Physics Engine & Polars AST Expressions
│   ├── NEURAL_PIPELINE.md      # Phi-4-mini Reasoning SLM & Neuro-Symbolic Resolver
│   ├── HARDWARE_AND_CUDA.md    # NVIDIA CUDA Loader, VRAM Offload & Fallback Engine
│   ├── SYSTEM_WORKFLOW.md      # 5-Phase End-to-End Data Transformation Lifecycle
│   ├── USER_GUIDE.md           # Step-by-Step Interactive Operations Manual
│   ├── DEVELOPER_GUIDES.md     # Developer Setup, Extensibility & Architecture Rules
│   ├── DEPLOYMENT_AND_PACKAGING.md # PyInstaller Builds, Docker & Desktop Packaging
│   ├── TESTING.md              # Automated Pytest Suite (>91% Coverage), Mocks & QA
│   └── API_REFERENCE.md        # Internal API Reference, Classes, Signals & Contracts
│
├── src/                        # Primary Source Code
│   ├── agent/                  # High-level agent orchestration (SLMEngine facade)
│   ├── controllers/            # Subsystem Controllers (Map, Sources, Info, Settings)
│   ├── core/                   # Dependency Injection (AppBuilder), Schemas, MapRenderer
│   ├── domain/                 # Domain Model (AppState SSOT, immutable Entities)
│   ├── etl/                    # SensorBatchProcessor & SQLite WAL StorageRepository
│   ├── models/                 # Quantized GGUF LLM models (Phi-4-mini)
│   ├── services/               # Importers, ParquetService, Polars MathEngine, Persistence
│   ├── slm/                    # Low-level SLM (llama.cpp, PromptBuilder, Parser, Resolver)
│   └── utils/                  # CUDALoader, I18nManager, SLMTelemetry, Config
│
├── ui/                         # PySide6 Desktop GUI Components
│   ├── editor/                 # Sensor-to-Topology mapping editor panel
│   ├── map/                    # Interactive vector QGraphicsView canvas
│   ├── settings/               # Hardware offload & settings dialogs
│   ├── shared/                 # Common reusable widgets & dialogs
│   ├── sources/                # Telemetry directory inspector & file tree
│   └── main_window.py          # Central desktop layout container
│
└── tests/                      # Automated Test Suite (160 tests, >91% coverage)
    ├── test_controllers/       # Controller mediator and signal tests
    ├── test_core/              # AppBuilder, schemas and scene rendering tests
    ├── test_domain/            # AppState state transitions and entity tests
    ├── test_etl/               # Batch processor, hashing, and WAL tests
    ├── test_services/          # Importers, Polars AST math, and Parquet export tests
    ├── test_slm/               # Prompt construction, <think> isolator, and resolver tests
    ├── test_ui/                # Headless PySide6 widgets and view tests
    └── test_utils/             # CUDA library loader and i18n tests
```

---

## 📖 System Dimensions & Knowledge Vault Navigation

### 1. Core Infrastructure & Data Engineering
- **[Architecture Deep-Dive](ARCHITECTURE.md)**: Exhaustive technical blueprint detailing clean MVC, Builder dependency injection pattern, and decoupled worker threads.
- **[High-Performance ETL Pipeline](ETL_PIPELINE.md)**: Specifications for multi-threaded sensor ingestion, `SensorBatchProcessor`, MD5 hash caching, and thread-safe SQLite WAL staging.
- **[Data Models & Schemas](DATA_MODELS.md)**: Specifications for immutable domain entities, Pydantic v2 `KinematicMap` contracts, and the unified Apache Parquet schema.
- **[Vector Physics Engine](MATH_ENGINE.md)**: Polars AST compiler (`pl.Expr`), SIMD vector operations, SI unit normalization, and harmonic mean speed calculations.

### 2. Artificial Intelligence & Neuro-Symbolic Inference
- **[Neural Pipeline & SLM Architecture](NEURAL_PIPELINE.md)**: Embedded Small Language Model integration (Phi-4-mini GGUF via `llama.cpp`), GPU layer offload, and context window sizing.
- **[Neuro-Symbolic Resolver](NEURAL_PIPELINE.md#neuro-symbolic-resolution)**: Mathematical and heuristic validation isolating `<think>` reasoning tokens and enforcing deterministic physical bounds.
- **[System Workflow Lifecycle](SYSTEM_WORKFLOW.md)**: Detailed 5-phase data transformation lifecycle (Topology Ingestion, Sensor Discovery, Mapping, ETL Staging, Parquet Gold Export).

### 3. Hardware Acceleration & Graphics
- **[Hardware & CUDA Acceleration](HARDWARE_AND_CUDA.md)**: Dynamic discovery and loading of NVIDIA CUDA shared libraries (`libcudart.so`, `libcublas.so`), GPU VRAM offload, and CPU fallback.
- **[Core Concepts & Day Zero Integration](CORE_CONCEPTS.md)**: Foundational principles of Day Zero data engineering, SUMO microscopic graphs, and downstream integration with CARINA and SYNAPSE.

### 4. Operations, Frontend & Quality Assurance
- **[User Guide & Operations Manual](USER_GUIDE.md)**: Step-by-step visual tutorial for navigating maps, pairing road directions, associating sensor fields, and compiling projects.
- **[Developer & Integration Guides](DEVELOPER_GUIDES.md)**: Setup instructions, coding standards, implementing custom sensor loaders, and testing conventions.
- **[Deployment & Packaging](DEPLOYMENT_AND_PACKAGING.md)**: Compiling standalone executables via `sfusion.spec`, Docker multi-stage builds, and desktop environment integration.
- **[Testing & Quality Assurance](TESTING.md)**: Comprehensive Pytest suite (160 tests, >91% coverage), headless Qt verification, and mock fixtures.
- **[Internal API Reference](API_REFERENCE.md)**: Technical specifications for domain state, service contracts, Qt signals, and controller mediation.

---

> 💡 **Obsidian Knowledge Graph:** This documentation suite maintains full native support for [Obsidian](https://obsidian.md/). Open the `SFUSION` repository folder as an Obsidian Vault to navigate the interactive technical graph and backlinks.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
