# 🔄 Changelog

All notable changes to the **SFusion Mapper** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
* Comprehensive technical documentation hub with dual **Obsidian-style Wikilinks** and GitHub markdown links across 6 languages (EN, PT-BR, ES, FR, RU, ZH).
* Extensive automated test suite expanded to **169 tests** across 10 modules, achieving **>91% total test coverage** (Frontend: **~97%**, Backend: **~89%**):
  * Headless offscreen Qt test environment (`QT_QPA_PLATFORM=offscreen`) in `tests/conftest.py` with global fixtures (`qapp`, `mock_i18n`, `mock_config`).
  * Full UI component test coverage (`tests/test_ui/`): `MainWindow`, `MapView`, `SourcesPanel`, `EditorPanel`, `SettingsDialog`, and `dialogs`.
  * Complete controller tests (`tests/test_controllers/`): `MainController`, `MapController`, `SourcesController`, `InfoController`, and `SettingsController`.
  * Dependency injection and graphics scene tests (`tests/test_core/`): `AppBuilder`, `MapRenderer`, and schema validation.
* Native Excel (`.xlsx`, `.xls`) support and intelligent CSV timestamp extraction added to `UniversalExtractor`.
* Rule-based heuristic fallback in `SLMEngine` via `NeuroSymbolicResolver` when local GGUF neural model is unavailable.

### Fixed
* Fixed `UnboundLocalError` in `src/core/app_builder.py` by scoping the `backend_i18n` import at the module level.
* Replaced deprecated Pydantic v1 `BaseModel.copy()` with `BaseModel.model_copy()` in `src/services/neural_transformer.py`.
* Resolved race condition in `MainController`: chained asynchronous `PersistenceService` ➔ `ETLService` ➔ `ParquetService` via Qt Signals (`configuration_saved`, `ingestion_finished`, `export_finished`).
* Centralized pipeline error propagation (`ingestion_error`, `export_error`, `configuration_error`) preventing UI lockups and orphaned temporary staging files.
* Fixed `AttributeError` in `SettingsController._on_save()` by correctly referencing `self._main_window`.
* Eliminated PySide6 `event.pos()` and `QMouseEvent` constructor deprecation warnings.

### Changed
* Removed orphaned `sentence-transformers` dependency from `requirements.txt` and `pyproject.toml`, trimming >1 GB of unused packages.
* Reconfigured `Dockerfile` to directly run the PySide6 application without PyInstaller / `sfusion.spec`.
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

---

<div align="center">
  <img src="docs/assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="48" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>Licensed under the <a href="LICENSE">GNU Affero General Public License v3.0</a>. © 2026 Noxfort Systems.</small>
</div>
