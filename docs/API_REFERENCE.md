# ⚡ SFusion Internal API & Class Reference

This document provides a comprehensive technical reference for the core Python classes, methods, and Qt Signals forming the internal API of **SFusion Mapper**.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](../ARCHITECTURE.md) | 🧪 [Testing Guide](TESTING.md)

---

## 1. Domain & State Management (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
Central Single Source of Truth (SSOT) inheriting from `PySide6.QtCore.QObject`.

#### Qt Signals
* `map_data_loaded`: Emitted when SUMO nodes and edges are populated in state.
* `data_sources_changed`: Emitted when new sensor directories are registered or removed.
* `data_association_changed`: Emitted when a sensor is linked to a road or set to Global.
* `association_mode_changed`: Emitted when switching interactive selection modes.
* `savable_state_changed(bool)`: Emitted with boolean flag indicating if dataset export is valid.

#### Key Methods
* `set_map_data(nodes: Dict[str, MapNode], edges: Dict[str, MapEdge]) -> None`
* `add_data_source(source: DataSource) -> None`
* `associate_selected_source_to_element(element_id: str) -> None`
* `get_edge_pair_id(edge_id: str) -> str | None`: Computes opposing road segment ID (e.g. `-edge_123`).
* `_is_savable() -> bool`: Returns `True` if map is loaded and all `LOCAL` sources are bound.

---

## 2. Processing & Services (`src/services/` & `src/etl/`)

### `MathEngine` (`src/services/math_engine.py`)
Vector physics engine executing exclusively on CPU and RAM.

* `compile_ast(schema: KinematicMap) -> List[pl.Expr]`:
  Compiles per-row Polars expressions normalizing speed ($km/h$), flow, distance ($km$), and time ($h$).
* `compile_aggregations(columns: List[str]) -> List[pl.Expr]`:
  Compiles aggregation expressions calculating Harmonic Mean Speed ($v_s$), flow rate ($q$), and physical density ($k = q / v_s$).

### `SensorBatchProcessor` (`src/etl/sensor_processor.py`)
Thread-isolated ingestion worker.

* `process_source(source: DataSource, db_path: str, staging_repo: ETLStorageRepository, transformer: NeuralTransformer) -> int`:
  Reads files with `UniversalExtractor`, computes MD5 checksums, compresses with `zlib` (level 6), applies `NeuralTransformer`, and writes to SQLite staging.

### `ETLStorageRepository` (`src/etl/storage_repository.py`)
Thread-safe SQLite DAO managing Write-Ahead Logging (WAL).

* `create_source_table(table_name: str) -> None`
* `insert_batch(table_name: str, records: List[Tuple]) -> None`:
  Executes thread-safe parameterized inserts guarded by `threading.Lock()`.
* `insert_raw_archive(source_id: str, filename: str, ext: str, md5: str, size: int, blob: bytes) -> None`

### `ParquetService` (`src/services/parquet_service.py`)
Gold-layer columnar exporter.

* `export_db_to_parquet(db_path: str, output_path: str | None = None) -> None`:
  Dispatches `ParquetExportWorker` onto `QThreadPool.globalInstance()`. Emits `export_finished` upon completion.

---

## 3. Neural & SLM Subsystem (`src/agent/` & `src/slm/`)

### `SLMEngine` (`src/agent/slm_engine.py`)
High-level AI facade for semantic schema discovery.

* `discover_schema(raw_text: str, assoc_type: str = "LOCAL") -> KinematicMap`:
  Extracts hierarchical keys, constructs system prompt, triggers `llama.cpp` inference, parses output JSON, and validates candidate columns with `NeuroSymbolicResolver`.

### `NeuroSymbolicResolver` (`src/slm/neuro_symbolic_resolver.py`)
Deterministic validator preventing hallucinations.

* `resolve(model_output: Dict[str, Any], raw_data: Dict[str, Any]) -> KinematicMap`:
  Matches column candidates against `SPEED_CANDIDATES`, `FLOW_CANDIDATES`, `INTENSITY_CANDIDATES`, deduces units of measurement, and computes confidence score.

---

## 4. Application Orchestration (`src/main_controller.py`)

### `MainController`
Mediator linking views, domain state, and asynchronous background services.

* `load_map(file_path: str) -> None`
* `add_data_source(folder_path: str) -> None`
* `generate_dataset(output_parquet_path: str) -> None`:
  Executes the 5-phase data transformation pipeline.
* `_cleanup_temp_files(staging_db_path: str) -> None`:
  Safely unlinks temporary `.db`, `-wal`, `-shm`, and `-journal` files.
* `save_project(file_path: str) -> None`
* `load_project(file_path: str) -> None`

---

## 🔗 Related Documentation
* [[docs/INDEX]] - Knowledge Base Map of Content
* [[ARCHITECTURE]] - Technical Architecture
* [[docs/DATA_MODELS]] - Entities and Schemas
* [[docs/ETL_PIPELINE]] - ETL Ingestion Subsystem
* [[docs/TESTING]] - Test Suite Guidelines

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
