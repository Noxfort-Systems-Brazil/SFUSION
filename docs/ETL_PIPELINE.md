# ⚡ High-Performance ETL Pipeline

The **SFusion ETL Pipeline** is a multi-threaded, memory-efficient data ingestion engine designed to transform massive volumes of heterogeneous urban sensor records into standardized, physics-normalized kinematic datasets ready for simulation and AI consumption.

> [!NOTE]
> For high-level system architecture and component interactions, see [[ARCHITECTURE]] and the end-to-end lifecycle in [[docs/SYSTEM_WORKFLOW]].

---

## 🏗️ Architectural Overview

The ETL subsystem sits at the boundary between raw sensor telemetry and downstream simulation engines (such as SUMO). Rather than persisting uncompressed, unindexed files or applying slow row-by-row Python transformations, SFusion utilizes a **three-tier Medallion ingestion pattern**:

```mermaid
flowchart LR
    A["Raw Sensor Data<br/>(CSV, JSON, Excel)"] --> B["SensorBatchProcessor<br/>(orjson, MD5, zlib)"]
    B --> C["NeuralTransformer<br/>+ MathEngine (Polars)"]
    C --> D["ETLStorageRepository<br/>(SQLite WAL Staging)"]
    D --> E["ParquetService<br/>(Gold Unified Dataset)"]

    style A fill:#2D3748,stroke:#4A5568,color:#fff
    style B fill:#3182CE,stroke:#2B6CB0,color:#fff
    style C fill:#805AD5,stroke:#6B46C1,color:#fff
    style D fill:#DD6B20,stroke:#C05621,color:#fff
    style E fill:#38A169,stroke:#2F855A,color:#fff
```

1. **Bronze Layer (Raw Storage & Audit)**: Raw files are compressed via `zlib`, hashed using MD5 for deduplication, and preserved in the `raw_data_storage` table.
2. **Silver Layer (Normalized Staging)**: Events are parsed with `orjson`, evaluated through the [[docs/MATH_ENGINE|MathEngine]] computational graph, and batched into thread-isolated sensor tables (`section_<source_name>`).
3. **Gold Layer (Columnar Export)**: The [[docs/DATA_MODELS#final-unified-parquet-schema|ParquetService]] flattens, enriches, and exports the unified time-series into high-throughput Apache Parquet format.

---

## 🧩 Core ETL Components

### 1. Ingestion Orchestrator (`src/services/etl_service.py`)

* **Class**: `ETLService` & `ETLWorker` (inherits from `QRunnable`)
* **Concurrency**: Managed via PySide6 `QThreadPool` combined with Python `concurrent.futures.ThreadPoolExecutor` for worker thread delegation.
* **Responsibilities**:
  * Orchestrates background execution without freezing the Qt GUI event loop.
  * Emits fine-grained Qt Signals: `progress(int)`, `total_calculated(int)`, `finished(str)`, and `error(str)`.
  * Controls batch sizing (`BATCH_SIZE = 500`) to guarantee predictable memory footprints.

```python
# Signal orchestration in ETLWorkerSignals
class ETLWorkerSignals(QObject):
    finished = Signal(str)
    progress = Signal(int)
    total_calculated = Signal(int)
    error = Signal(str)
```

### 2. Sensor Batch Processor (`src/etl/sensor_processor.py`)

* **Class**: `SensorBatchProcessor`
* **Responsibilities**:
  * Implements **Single Responsibility Principle (SRP)** by staying decoupled from database connections and UI states.
  * Ingests files using `UniversalExtractor` ([src/services/extractors.py](file:///home/gabriel-moraes/Documentos/SFUSION/src/services/extractors.py)) with C-accelerated `orjson` when available.
  * Calculates binary checksums (`hashlib.md5`) and compresses file payloads with `zlib.compress(level=6)`.
  * Passes extracted raw dictionaries through [[docs/NEURAL_PIPELINE|NeuralTransformer]] to inject normalized kinematic fields (`speed_val`, `flow_val`, `intensity_val`).

### 3. Storage Repository & SQLite Concurrency (`src/etl/storage_repository.py`)

* **Class**: `ETLStorageRepository`
* **Design Pattern**: Data Access Object (DAO) / Repository Pattern.
* **Concurrency Tuning**:
  * SQLite is configured in **Write-Ahead Logging (WAL)** mode:
    ```sql
    PRAGMA journal_mode = WAL;
    PRAGMA busy_timeout = 120000;
    PRAGMA synchronous = NORMAL;
    PRAGMA cache_size = -64000;  -- 64MB shared page cache
    PRAGMA temp_store = MEMORY;
    ```
  * Thread-safe atomic transactions wrapped in a mutual exclusion lock (`threading.Lock`), preventing `SQLITE_BUSY` database lock errors under high write contention.

---

## 🗄️ Staging Database Lifecycle & Cleanup

To deliver extreme performance without leaving multi-gigabyte temporary files on the user's filesystem:

1. When the user clicks **"Generate Dataset"**, a hidden staging database is created:
   ```python
   staging_db = os.path.join(output_dir, f".temp_sfusion_{base_name}.db")
   ```
2. The [[docs/DATA_MODELS#application-state-and-persistence|PersistenceService]] populates the network metadata (`node_metadata`, `edge_metadata`, `data_associations`).
3. The `ETLService` processes all registered data sources into `section_<name>` tables.
4. Upon ingestion completion, `ParquetService` reads the staging database, formats the final `.parquet` file, and closes all open connections.
5. The method `MainController._cleanup_temp_files()` unlinks the staging database and all auxiliary files (`.db`, `-wal`, `-shm`, `-journal`).

---

## 🔗 Related Documentation
* [[docs/INDEX]] - Knowledge Base Map of Content
* [[ARCHITECTURE]] - High-level MVC and layer separation
* [[docs/MATH_ENGINE]] - Vector physics compilation and SI unit normalization
* [[docs/SYSTEM_WORKFLOW]] - End-to-end system workflow
* [[docs/DATA_MODELS]] - Schema definitions and Parquet specifications
