# ⚡ 高性能 ETL 摄取流水线

**SFusion ETL 流水线** 是一个高并发、低内存开销的数据抽取转换引擎，专为将海量异构传感器原始记录转换为标准化物理数据集而设计。

⬅️ [文档中心](README.md) | 🏛️ [系统架构](architecture.md) | 📐 [矢量物理引擎](math_engine.md)

---

## 1. 三层奖章式流转体系

```mermaid
flowchart LR
    A["原始数据源"] --> B["SensorBatchProcessor (MD5, zlib)"]
    B --> C["NeuralTransformer + MathEngine (Polars)"]
    C --> D["ETLStorageRepository (SQLite WAL)"]
    D --> E["ParquetService (金标 Parquet 数据集)"]
```

1. **铜级存储 (Bronze)**：原始数据经 zlib 高速压缩（level 6）与 MD5 防重校验，完整持久化于 `raw_data_storage` 表中。
2. **银级暂存 (Silver)**：记录经由 C 语言加速的 `orjson` 解码，并应用 `MathEngine` 矢量物理图计算，分表写入 `section_<name>`。
3. **金标导出 (Gold)**：`ParquetService` 展开字段、合并地理元数据，导出具备极高压缩比的 Snappy 压缩 Parquet 文件。

---

## 2. SQLite WAL 高并发读写调优

持久化存储仓库针对多线程环境进行了深度优化：
```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 120000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB 共享内存缓存
PRAGMA temp_store = MEMORY;
```
批量写入全部在线程级互斥锁（`threading.Lock()`）保护下原子化提交，彻底杜绝高频写入导致的 `SQLITE_BUSY` 数据库锁死异常。

---

## 3. 临时暂存库生命周期自动化回收

当用户点击“生成数据集”时，系统会在目标目录生成隐藏暂存库 `.temp_sfusion_<name>.db`。Parquet 编译完成后，控制器自动触发 `_cleanup_temp_files()`，彻底删除临时库及其附带的 WAL 与共享内存文件（`.db`, `-wal`, `-shm`）。

---

## 🔗 相关技术文档
* [文档中心首页](README.md)
* [数据模型规范](data_models.md)
* [系统工作流](system_workflow.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>卓越科技 • A State Of Art Company</i><br/>
  <i>智慧交通出行工程 • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. 基于 AGPLv3 协议授权.</small>
</div>
