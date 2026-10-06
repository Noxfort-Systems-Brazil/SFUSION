# 🔄 System Workflow & Data Lifecycle

The **SFusion Mapper** follows a deterministic, 5-phase lifecycle that transforms raw user inputs and unaligned sensor streams into an actionable, physics-validated **Apache Parquet dataset**.

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | 🖥️ [User Guide](user_guide.md)

---

## 1. End-to-End Workflow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as PySide6 GUI
    participant AppState as AppState (SSOT)
    participant SLM as SLMEngine (Phi-4-mini)
    participant ETL as ETLService & StorageRepo
    participant Parquet as ParquetService

    User->>UI: 1. Import SUMO Network (.net.xml)
    UI->>AppState: Load Nodes & Edges (MapImporter)
    AppState-->>UI: Render Topology (MapRenderer)

    User->>UI: 2. Add Sensor Source Directory
    UI->>AppState: Register DataSource (DataImporter)

    User->>UI: 3. Associate Source with Road / Global
    UI->>SLM: Trigger Schema Discovery
    SLM-->>UI: Populate KinematicMap Blueprint
    User->>UI: (Optional) Validate or Override Schema

    User->>UI: 4. Click "Generate Dataset"
    UI->>AppState: Create Temp Staging DB (.temp_sfusion_*.db)
    UI->>ETL: Ingest & Apply Vector Physics (MathEngine)
    ETL-->>UI: Progress Updates (Signals)

    ETL->>Parquet: Ingestion Complete Trigger
    Parquet->>Parquet: Build Unified Columnar Dataset (.parquet)
    Parquet->>UI: 5. Purge Staging DB & Notify Success
```

---

## 2. Detailed Transformation Phases

### Phase 1: Map Topology Ingestion
* User selects standard `.net.xml` or compressed `.net.xml.gz` road network.
* `MapImporter` extracts junctions (`MapNode`) and directional roads (`MapEdge`).
* `AppState` stores the topology and `MapRenderer` draws the vector network on the PySide6 canvas.

### Phase 2: Data Source Registration
* User selects a folder containing sensor files (CSV, JSON, XML, Excel).
* `DataImporter` inspects headers, detects file formats, and registers a `DataSource` entity in `AppState`.

### Phase 3: Association & Neuro-Symbolic Discovery
* User associates a sensor with a road edge (Local) or applies it across the network (Global).
* `SLMEngine` prompts *Phi-4-mini* to infer semantic column mappings.
* `NeuroSymbolicResolver` validates candidates, assigns physical units, and generates the `KinematicMap` blueprint.

### Phase 4: Staging ETL Ingestion
* User clicks "Generate Dataset".
* Hidden SQLite staging database is created (`.temp_sfusion_<name>.db`).
* Multi-threaded `SensorBatchProcessor` compresses raw archives into Bronze storage, parses events into Silver staging tables, and evaluates Polars AST expressions in parallel.

### Phase 5: Columnar Export & Cleanup
* `ParquetService` consolidates all Silver tables, joins spatial metadata, formats timestamps in UTC, and writes the final Snappy-compressed Apache Parquet dataset.
* `MainController._cleanup_temp_files()` unlinks all temporary staging database files.

---

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [ETL Pipeline](etl_pipeline.md)
* [User Guide](user_guide.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under AGPLv3.</small>
</div>
