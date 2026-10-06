# ⚡ 内部核心 API 与类参考手册

本文档系统性定义 **SFusion Mapper** 核心 Python 类、公共方法契约及 Qt 信号规范。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 🧪 [测试指南](testing.md)

---

## 1. 状态机与领域模型 (`src/domain/`)

### `AppState` (`src/domain/app_state.py`)
* **核心信号**: `map_data_loaded`、`data_sources_changed`、`data_association_changed`、`savable_state_changed(bool)`。
* **主要方法**: `set_map_data()`、`add_data_source()`、`associate_selected_source_to_element()`、`_is_savable()`。

---

## 2. 计算与数据服务 (`src/services/` & `src/etl/`)

* **`MathEngine`**: `compile_ast()` 与 `compile_aggregations()`。
* **`SensorBatchProcessor`**: `process_source()`。
* **`ETLStorageRepository`**: `create_source_table()` 与 `insert_batch()`。
* **`ParquetService`**: `export_db_to_parquet()`。
* **`SLMEngine`**: `discover_schema()`。
* **`MainController`**: `load_map()`、`generate_dataset()`、`_cleanup_temp_files()`。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [系统架构](architecture.md)
* [测试指南](testing.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
