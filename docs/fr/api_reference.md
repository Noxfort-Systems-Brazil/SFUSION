# ⚡ Référence de l'API Interne

Spécification formelle des classes, méthodes et signaux centraux de **SFusion Mapper**.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🧪 [Tests](testing.md)

---

## 1. État et Domaine (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
* **Signaux** : `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed(bool)`.
* **Méthodes** : `set_map_data()`, `add_data_source()`, `associate_selected_source_to_element()`, `_is_savable()`.

---

## 2. Traitement et Services (`src/services/` & `src/etl/`)

* **`MathEngine`** : `compile_ast()` et `compile_aggregations()`.
* **`SensorBatchProcessor`** : `process_source()`.
* **`ETLStorageRepository`** : `create_source_table()`, `insert_batch()`.
* **`ParquetService`** : `export_db_to_parquet()`.
* **`SLMEngine`** : `discover_schema()`.
* **`MainController`** : `load_map()`, `generate_dataset()`, `_cleanup_temp_files()`.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Architecture](architecture.md)
* [Tests](testing.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Sous licence AGPLv3.</small>
</div>
