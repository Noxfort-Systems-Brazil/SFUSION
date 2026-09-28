# ⚡ Referência da API Interna e Classes

Este documento fornece a especificação técnica formal das principais classes, métodos e Sinais Qt que constituem a API interna do **SFusion Mapper**.

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | 🧪 [Testes](testing.md)

---

## 1. Gestão de Estado e Domínio (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
Fonte Única da Verdade (SSOT) herdando de `PySide6.QtCore.QObject`.

* **Sinais Qt**: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `association_mode_changed`, `savable_state_changed(bool)`.
* **Principais Métodos**:
  * `set_map_data(nodes: Dict[str, MapNode], edges: Dict[str, MapEdge]) -> None`
  * `add_data_source(source: DataSource) -> None`
  * `associate_selected_source_to_element(element_id: str) -> None`
  * `get_edge_pair_id(edge_id: str) -> str | None`
  * `_is_savable() -> bool`

---

## 2. Serviços de Processamento (`src/services/` & `src/etl/`)

### `MathEngine` (`src/services/math_engine.py`)
* `compile_ast(schema: KinematicMap) -> List[pl.Expr]`:
  Compila expressões Polars que convertem velocidades para km/h, distâncias para km e tempos para horas.
* `compile_aggregations(columns: List[str]) -> List[pl.Expr]`:
  Calcula a Velocidade Média Espacial (Harmônica), a vazão ($q$) e a densidade física ($k = q / v$).

### `SensorBatchProcessor` (`src/etl/sensor_processor.py`)
* `process_source(source, db_path, staging_repo, transformer) -> int`:
  Executa leitura em disco, hashing MD5, compressão zlib e normalização de payloads na base de staging.

### `ETLStorageRepository` (`src/etl/storage_repository.py`)
* `create_source_table(table_name: str) -> None`
* `insert_batch(table_name: str, records: List[Tuple]) -> None`
* `insert_raw_archive(source_id: str, filename: str, ext: str, md5: str, size: int, blob: bytes) -> None`

### `ParquetService` (`src/services/parquet_service.py`)
* `export_db_to_parquet(db_path: str, output_path: str | None = None) -> None`:
  Executa `ParquetExportWorker` assincronamente no `QThreadPool.globalInstance()`.

---

## 3. Subsistema Neural e SLM (`src/agent/` & `src/slm/`)

### `SLMEngine` (`src/agent/slm_engine.py`)
* `discover_schema(raw_text: str, assoc_type: str = "LOCAL") -> KinematicMap`

### `NeuroSymbolicResolver` (`src/slm/neuro_symbolic_resolver.py`)
* `resolve(model_output: Dict[str, Any], raw_data: Dict[str, Any]) -> KinematicMap`

---

## 4. Orquestração da Aplicação (`src/main_controller.py`)

### `MainController`
* `load_map(file_path: str) -> None`
* `add_data_source(folder_path: str) -> None`
* `generate_dataset(output_parquet_path: str) -> None`
* `_cleanup_temp_files(staging_db_path: str) -> None`
* `save_project(file_path: str) -> None`
* `load_project(file_path: str) -> None`

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Arquitetura](architecture.md)
* [Diretrizes de Testes](testing.md)
