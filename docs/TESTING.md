# 🧪 Testing & Quality Assurance Guidelines

SFusion operates as the deterministic "Day Zero" transformation engine for urban simulation and machine learning pipelines. High data reliability, thread-safety in SQLite staging, and mathematical precision in kinematic unit conversions require thorough automated testing.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](../ARCHITECTURE.md) | 📐 [Math Engine](MATH_ENGINE.md)

---

## 1. Test Suite Execution

### 1.1 Running All Automated Tests
Using the project's local virtual environment:
```bash
./.venv/bin/pytest tests/ -v
```

### 1.2 Generating Code Coverage Reports
To measure statement and branch coverage across all modules in `src/`:
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```
The interactive HTML coverage report will be generated at `htmlcov/index.html`.

### 1.3 Running Specific Test Modules
```bash
# Test the Polars vector physics engine
./.venv/bin/pytest tests/test_services/test_math_engine.py -v

# Test the reactive domain application state
./.venv/bin/pytest tests/test_domain/test_app_state.py -v

# Test the multi-threaded ETL sensor processor
./.venv/bin/pytest tests/test_etl/test_sensor_processor.py -v

# Test CUDA discovery hooks and dynamic library loader
./.venv/bin/pytest tests/test_utils/test_cuda_loader.py -v
```

---

## 2. Test Suite Architecture (66 Tests Across 8 Modules)

The test suite in `tests/` contains **66 automated tests** providing complete coverage of domain rules, data contracts, ETL concurrency, and AI schema parsing:

| Test Module | Test File | Target Under Test | Tested Behaviors |
| :--- | :--- | :--- | :--- |
| **SLM Agent** | `test_slm_engine.py` | `SLMEngine` Facade | Schema discovery orchestration, prompt formatting, mock inference handling, and fallback behavior. |
| **Controllers** | `test_main_controller.py` | `MainController` | Lifecycle coordination, project load/save, staging database creation (`.temp_sfusion_*.db`), and automated cleanup. |
| **Core Schemas** | `test_schemas.py` | `KinematicMap` (Pydantic) | Typed schema validation, field default constraints, unit enumeration, and serialization. |
| **Domain Models** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Reactive Qt signal dispatch (`map_data_loaded`, `data_sources_changed`), directional road pairing, and `_is_savable()` invariant enforcement. |
| **ETL Subsystem** | `test_sensor_processor.py`<br/>`test_storage_repository.py` | `SensorBatchProcessor`<br/>`ETLStorageRepository` | Multi-threaded extraction, MD5 hashing, zlib compression, SQLite WAL PRAGMAs, and thread-safe batch transactions. |
| **Services Layer** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Service Workers | Polars AST compilation, SI unit conversion ($km/h$, $m/s$, $mph$), harmonic mean speed, Parquet export, SUMO XML parsing, and `.sfm.json` serialization. |
| **SLM Parsing** | `test_slm_output_parser.py` | `SLMOutputParser` | Robust extraction of pure JSON payloads from model output, stripping `<think>...</think>` internal reasoning tags, markdown fences, and preambles. |
| **Utilities** | `test_cuda_loader.py` | `cuda_loader.py` | Discovery of pip-bundled CUDA shared objects (`libcudart.so`, `libcublas.so`), dynamic library preloading, and CPU fallback. |

---

## 3. Mocking & Isolation Strategy

1. **GUI Decoupling**: Qt widgets are isolated from business logic. Tests verify `AppState` signals and controller methods without requiring an active X11/Wayland display server.
2. **Inference Mocking**: Unit tests for `SLMEngine` and `NeuroSymbolicResolver` use deterministic JSON fixtures, allowing tests to run rapidly in CI/CD without requiring 4GB VRAM GPU hardware.
3. **In-Memory SQLite Staging**: Storage repository tests utilize temporary or in-memory SQLite instances to verify concurrency and WAL locks safely.
4. **Temporary File Sandboxing**: All file export tests write to pytest's `tmp_path` fixture and verify automated unlinking upon completion.

---

## 🔗 Related Documentation
* [[docs/INDEX]] - Knowledge Base Map of Content
* [[ARCHITECTURE]] - Technical Architecture
* [[docs/MATH_ENGINE]] - Vector Physics and AST Compilation
* [[docs/ETL_PIPELINE]] - High-Performance ETL Engine
* [[docs/API_REFERENCE]] - Public API and Class Reference
