# 🧪 Testing & Quality Assurance Guidelines

SFusion operates as the deterministic "Day Zero" transformation engine for urban simulation and machine learning pipelines. High data reliability, thread-safety in SQLite staging, and mathematical precision in kinematic unit conversions require thorough automated testing.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [API Reference](api_reference.md)

---

## 1. Test Suite Execution

### 1.1 Running All Automated Tests
```bash
./.venv/bin/pytest tests/ -v
```

### 1.2 Generating Code Coverage Reports
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. Test Architecture (66 Tests Across 8 Modules)

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

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [Technical Architecture](architecture.md)
* [API Reference](api_reference.md)
