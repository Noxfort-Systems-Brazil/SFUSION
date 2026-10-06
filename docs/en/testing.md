# 🧪 Testing & Quality Assurance Guidelines

SFusion operates as the deterministic "Day Zero" transformation engine for urban simulation and machine learning pipelines. High data reliability, thread-safety in SQLite staging, and mathematical precision in kinematic unit conversions require thorough automated testing.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [API Reference](api_reference.md)

---

## 1. Test Suite Execution

### 1.1 Running All Automated Tests
Using the project's local virtual environment with headless offscreen Qt:
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 Generating Code Coverage Reports
To measure statement and branch coverage across both backend (`src/`) and frontend (`ui/`):
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
The interactive HTML coverage report will be generated at `htmlcov/index.html`. SFusion achieves **>91% total code coverage** (Frontend: **~97%**, Backend: **~89%**).

---

## 2. Test Architecture (160 Tests Across 10 Modules)

The test suite in `tests/` contains **160 automated tests** providing >91% coverage across domain rules, frontend views, controllers, data contracts, ETL concurrency, and AI schema parsing:

| Test Module | Test File | Target Under Test | Tested Behaviors |
| :--- | :--- | :--- | :--- |
| **Frontend Views** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_main_window.py` | UI Components (`ui/`) | Offscreen headless Qt interaction, widget layouts, signals/slots, list selection, contextual menus, mouse panning/zooming, and modal configurations (~97% coverage). |
| **Controllers** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | Controllers (`src/controllers/`) | Multi-phase pipeline coordination (Persistence -> ETL -> Parquet -> Cleanup), visual highlighting, road pairing, and model synchronization. |
| **Core & DI** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder & Renderer | Full dependency injection wiring, QGraphicsScene drawing (ribbon stroker, junctions, directional arrows), and Pydantic schema validation. |
| **SLM Agent & Reasoning** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | SLM Pipeline (`src/slm/`) | Deterministic unit inference, heuristic schema disambiguation, hierarchical key extraction, token filtering, and prompt synthesis. |
| **Domain Models** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Reactive Qt signal dispatch (`map_data_loaded`, `data_sources_changed`), directional road pairing, association management, and `_is_savable()` invariant enforcement. |
| **ETL Subsystem** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL & Transformers | Multi-threaded extraction, MD5 hashing, zlib compression, SQLite WAL PRAGMAs, payload flattening, and Polars AST physics compilation. |
| **Services Layer** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Service Workers | Polars AST compilation, SI unit conversion ($km/h$, $m/s$, $mph$), harmonic mean speed, Parquet export, SUMO XML/GZ parsing, and `.sfm.json` serialization. |
| **Utilities** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | Utils & Hardware | Configuration persistence, nested translation resolution, CPU/VRAM telemetry, CUDA shared object discovery, and dynamic fallback. |

---

## 3. Mocking & Isolation Strategy

1. **Headless Offscreen Qt Platform**: PySide6 widgets are initialized and tested headlessly using `QT_QPA_PLATFORM=offscreen`. `tests/conftest.py` configures a shared `QApplication` fixture (`qapp`) and mocks for translations (`mock_i18n`) and application settings (`mock_config`), preventing UI windows from blocking CI test runners.
2. **Deterministic SLM Fixtures**: Unit tests for `SLMEngine`, `LLMInferenceProvider`, and `NeuroSymbolicResolver` use deterministic JSON fixtures and unittest mocks, verifying semantic column resolution without requiring an active GPU or 3.5GB model weights.
3. **In-Memory & Staging SQLite Isolation**: ETL and storage repository tests use temporary SQLite databases with WAL mode enabled, verifying concurrent multi-threaded writes without persisting artifacts to disk.
4. **Temporary File Sandboxing**: All file generation tests (project `.sfm.json`, staging SQLite DBs, and exported Apache Parquet datasets) execute within pytest's `tmp_path` fixture with verified unlinking.
5. **Process Exit Guarding**: `MainWindow.closeEvent` invokes `os._exit(0)` in production; tests isolate this behavior using `monkeypatch.setattr(os, "_exit", mock_exit)` to ensure clean teardown without aborting the test runner.

---

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [Technical Architecture](architecture.md)
* [API Reference](api_reference.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under AGPLv3.</small>
</div>
