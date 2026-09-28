# ⚡ SFusion Internal API & Class Reference

This document provides a comprehensive technical reference for the core Python classes, methods, and Qt Signals forming the internal API of **SFusion Mapper**.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | 🧪 [Testing Guide](testing.md)

---

## 1. Domain & State Management (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
Central Single Source of Truth (SSOT) inheriting from `PySide6.QtCore.QObject`.

* **Signals**: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `association_mode_changed`, `savable_state_changed(bool)`.
* **Key Methods**:
  * `set_map_data(nodes: Dict[str, MapNode], edges: Dict[str, MapEdge]) -> None`
  * `add_data_source(source: DataSource) -> None`
  * `associate_selected_source_to_element(element_id: str) -> None`
  * `get_edge_pair_id(edge_id: str) -> str | None`
  * `_is_savable() -> bool`

---

## 2. Processing & Services (`src/services/` & `src/etl/`)

### `MathEngine` (`src/services/math_engine.py`)
* `compile_ast(schema: KinematicMap) -> List[pl.Expr]`:
  Translates blueprint to Polars expressions normalizing speed to km/h, distance to km, and time to hours.
* `compile_aggregations(columns: List[str]) -> List[pl.Expr]`:
  Calculates Space Mean Speed (Harmonic Mean), flow throughput ($q$), and physical density ($k = q / v$).

### `SensorBatchProcessor` (`src/etl/sensor_processor.py`)
* `process_source(source, db_path, staging_repo, transformer) -> int`:
  Executes file I/O, MD5 checksum calculation, zlib compression, and normalizes payloads into SQLite staging tables.

### `ETLStorageRepository` (`src/etl/storage_repository.py`)
* `create_source_table(table_name: str) -> None`
* `insert_batch(table_name: str, records: List[Tuple]) -> None`
* `insert_raw_archive(source_id: str, filename: str, ext: str, md5: str, size: int, blob: bytes) -> None`

### `ParquetService` (`src/services/parquet_service.py`)
* `export_db_to_parquet(db_path: str, output_path: str | None = None) -> None`:
  Executes `ParquetExportWorker` asynchronously on `QThreadPool.globalInstance()`.

---

## 3. Neural & SLM Subsystem (`src/agent/` & `src/slm/`)

### `SLMEngine` (`src/agent/slm_engine.py`)
* `discover_schema(raw_text: str, assoc_type: str = "LOCAL") -> KinematicMap`

### `NeuroSymbolicResolver` (`src/slm/neuro_symbolic_resolver.py`)
* `resolve(model_output: Dict[str, Any], raw_data: Dict[str, Any]) -> KinematicMap`

---

## 4. Application Orchestration (`src/main_controller.py`)

### `MainController`
* `load_map(file_path: str) -> None`
* `add_data_source(folder_path: str) -> None`
* `generate_dataset(output_parquet_path: str) -> None`
* `_cleanup_temp_files(staging_db_path: str) -> None`
* `save_project(file_path: str) -> None`
* `load_project(file_path: str) -> None`

---

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [Architecture](architecture.md)
* [Testing Guide](testing.md)
