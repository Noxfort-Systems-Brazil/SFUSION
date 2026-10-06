# 🖥️ User Guide & Operations Manual

This guide walks you through the complete end-to-end operational procedure for using the **SFusion Mapper** Graphical User Interface (GUI).

⬅️ [Documentation Hub](README.md) | 🏛️ [Architecture](architecture.md) | 🔄 [System Workflow](system_workflow.md)

---

## 1. Interface Zones

The SFusion Mapper interface is organized into three primary functional zones:

```text
+-------------------------------------------------------------------------+
| Toolbar: [Open Project] [Save Project] | [Open Map] [Add Source] | [Generate Dataset] | [Settings]
+-------------------+--------------------------------+--------------------+
|                   |                                |                    |
|   Sources Panel   |            Map View            |    Editor Panel    |
|   (Left Sidebar)  |        (Central Canvas)        |  (Right Sidebar)   |
|                   |                                |                    |
| - Data Sources    | - Interactive SUMO Network     | - Inferred Schema  |
| - Local / Global  | - Junctions (Nodes)            | - Physical Units   |
| - Association     | - Directional Roads (Edges)    | - Manual Override  |
|                   | - Edge Pair Highlighting       | - Real Road Names  |
|                   |                                |                    |
+-------------------+--------------------------------+--------------------+
| Status Bar: Ready / Progress / System Telemetry                         |
+-------------------------------------------------------------------------+
```

---

## 2. Step-by-Step Operation

### Step 1: Importing the Network Topology
1. Click **Open Map** on the toolbar (or press `Ctrl+M`).
2. Select your SUMO file (`.net.xml` or `.net.xml.gz`).
3. Navigate the canvas: Scroll wheel to zoom, click and drag on background to pan.

### Step 2: Adding Sensor Folders
1. Click **Add Source** on the toolbar.
2. Choose a directory containing your raw sensor files.
3. The dataset appears in the left **Sources Panel** with detected format badges.

### Step 3: Configuring Associations
* **Local Association**: Select the data source, click **Associate**, then click the target road on the map. Opposing road segments are automatically detected and paired.
* **Global Association**: Right-click the data source in the list and select **Set as Global**.

### Step 4: Validating & Overriding AI Schemas
1. Inspect inferred columns in the right-hand **Editor Panel**.
2. If necessary, use dropdowns to manually reassign speed, flow, or intensity fields.
3. Assign human-readable street names (e.g. *"Main Avenue"*) to enrich Parquet outputs.
4. Click **Save** in the Editor Panel.

### Step 5: Generating the Final Dataset
1. When all local sources are mapped, click **Generate Dataset**.
2. Choose an output directory and filename (e.g. `traffic_dataset.parquet`).
3. Monitor the progress bar during ingestion and export.

### Step 6: Session Management
* Click **Save Project** to export mapping configurations to `.sfm.json`.
* Click **Open Project** to resume saved work sessions instantly.

---

## 🔗 Related Documentation
* [Documentation Hub](README.md)
* [System Workflow](system_workflow.md)
* [Data Models](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Smart Mobility Engineering • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licensed under AGPLv3.</small>
</div>
