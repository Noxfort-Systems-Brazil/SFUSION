# ⚡ Referencia de la API Interna

Especificación formal de clases, métodos y señales del núcleo de **SFusion Mapper**.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 🧪 [Pruebas](testing.md)

---

## 1. Estado y Dominio (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
* **Señales**: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed(bool)`.
* **Métodos**: `set_map_data()`, `add_data_source()`, `associate_selected_source_to_element()`, `_is_savable()`.

---

## 2. Procesamiento y Servicios (`src/services/` & `src/etl/`)

* **`MathEngine`**: `compile_ast()` y `compile_aggregations()`.
* **`SensorBatchProcessor`**: `process_source()`.
* **`ETLStorageRepository`**: `create_source_table()`, `insert_batch()`.
* **`ParquetService`**: `export_db_to_parquet()`.
* **`SLMEngine`**: `discover_schema()`.
* **`MainController`**: `load_map()`, `generate_dataset()`, `_cleanup_temp_files()`.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Arquitectura](architecture.md)
* [Pruebas](testing.md)
