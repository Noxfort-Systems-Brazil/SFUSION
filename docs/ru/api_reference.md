# ⚡ Спецификация внутреннего API

Техническое описание ключевых классов, методов и сигналов ядра **SFusion Mapper**.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | 🧪 [Тестирование](testing.md)

---

## 1. Состояние и доменная модель (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
* **Сигналы**: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed(bool)`.
* **Методы**: `set_map_data()`, `add_data_source()`, `associate_selected_source_to_element()`, `_is_savable()`.

---

## 2. Сервисы обработки данных (`src/services/` & `src/etl/`)

* **`MathEngine`**: `compile_ast()` и `compile_aggregations()`.
* **`SensorBatchProcessor`**: `process_source()`.
* **`ETLStorageRepository`**: `create_source_table()`, `insert_batch()`.
* **`ParquetService`**: `export_db_to_parquet()`.
* **`SLMEngine`**: `discover_schema()`.
* **`MainController`**: `load_map()`, `generate_dataset()`, `_cleanup_temp_files()`.

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Архитектура](architecture.md)
* [Тестирование](testing.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Инженерия интеллектуальной мобильности • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Лицензия AGPLv3.</small>
</div>
