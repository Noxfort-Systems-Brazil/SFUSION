# 🔄 Changelog

All notable changes to the **SFusion Mapper** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
* Comprehensive technical documentation hub in English with dual **Obsidian-style Wikilinks** and GitHub markdown links:
  * Master Map of Content: [[docs/INDEX]].
  * In-depth [[docs/ETL_PIPELINE]] guide explaining multi-threaded ingestion and SQLite WAL concurrency.
  * In-depth [[docs/MATH_ENGINE]] guide detailing Polars AST compilation and SI unit normalization.
  * Dedicated [[docs/HARDWARE_AND_CUDA]] guide covering GPU offload and dynamic CUDA discovery.
* Comprehensive unit test suite across domain, controllers, services, ETL, SLM, and utility layers (16 test suites).

### Changed
* Synchronized `pyproject.toml` dependencies with production requirements (`polars`, `pyarrow`, `pydantic`, `sentence-transformers`, `numpy`, `llama-cpp-python`).
* Clarified export lifecycle in documentation: the application exports an **Apache Parquet (`.parquet`)** dataset with SQLite acting as a temporary, self-cleaning staging database.

---

## [0.1.0] - 2026-06-15

### Added
* **Apache Parquet Columnar Exporter**: Integrated `ParquetService` and `ParquetExportWorker` for exporting unified traffic time-series datasets.
* **Vector Physics Engine (`MathEngine`)**: Built-in AST compiler using **Polars** (`pl.Expr`) to normalize speed ($km/h$), distance ($km$), time ($h$), flow ($veh/h$), and intensity into standard SI/SUMO units.
* **Multi-Threaded ETL Ingestion**: Implemented `SensorBatchProcessor` (MD5 hashing, zlib compression, orjson extraction) and `ETLStorageRepository` (thread-safe SQLite WAL transactions).
* **Neuro-Symbolic SLM Subsystem**: Decomposed AI schema discovery into four modular services:
  * `LLMInferenceProvider`: Low-level `llama.cpp` integration with GPU offloading and FlashAttention.
  * `SchemaPromptBuilder`: Hierarchical dotted property traversal for JSON and CSV headers.
  * `SLMOutputParser`: Resilient reasoning token isolation (`<think>`) and JSON sanitization.
  * `NeuroSymbolicResolver`: Heuristic candidate validation and unit deduction.
* **CUDA Dynamic Library Discovery (`cuda_loader.py`)**: Automatic discovery and preloading of bundled NVIDIA runtime libraries (`libcudart.so`, `libcublas.so`).
* **Dual Internationalization Architecture**: Divided translations into `locale/` (PySide6 UI) and `locale_backend/` (logs and background workers) across 6 languages (EN, PT-BR, ES, FR, RU, ZH).
* **Interactive SUMO Topology Canvas**: Vectorized network visualization supporting junction nodes, road edges, pan/zoom, and intelligent bidirectional edge pair grouping.

---

*Return to [[README]] or [[docs/INDEX]]*
