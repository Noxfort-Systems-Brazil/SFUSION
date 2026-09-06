# 📚 SFusion Knowledge Base (MOC)

Welcome to the central **Map of Content (MOC)** for **SFusion Mapper**. This knowledge base organizes the conceptual, mathematical, architectural, and operational documentation of the ecosystem. All documents are interconnected using dual **Obsidian-style Wikilinks** and **GitHub-compatible Markdown links** for seamless graph visualization and web browsing.

---

## 🧭 Navigation Hub

| Section | Description | Key Documents |
| :--- | :--- | :--- |
| **🚀 Project Foundation** | Project overview, quick start, architecture, and standards | [[README\|Project Overview]] • [[ARCHITECTURE\|Technical Architecture]] • [[CHANGELOG\|Version History]] • [[CONTRIBUTING\|Contribution Guide]] • [[CODE_OF_CONDUCT\|Code of Conduct]] |
| **📖 Core Concepts & Data** | Fundamental ideas, state management, and schema blueprints | [[docs/CORE_CONCEPTS\|Core Concepts]] • [[docs/SYSTEM_WORKFLOW\|System Workflow]] • [[docs/DATA_MODELS\|Data Models & Schemas]] |
| **⚡ Processing Engines** | High-performance ETL, vector compilation, and AI inference | [[docs/ETL_PIPELINE\|ETL Pipeline]] • [[docs/MATH_ENGINE\|Vector Physics Engine]] • [[docs/NEURAL_PIPELINE\|Neural Pipeline & SLM]] • [[docs/HARDWARE_AND_CUDA\|Hardware & CUDA]] |
| **🖥️ Guides & Operations** | Operational manual for GUI usage and configurations | [[docs/USER_GUIDE\|User Guide]] |

---

## 🗺️ Detailed Document Directory

### 1. Foundation & Architecture
* [[README]] — High-level introduction, key features, prerequisites, and getting started.
* [[ARCHITECTURE]] — Model-View-Controller (MVC), Builder pattern, dependency injection, and layer separation.
* [[CHANGELOG]] — Semantic versioning tracking additions, optimizations, and breaking changes.
* [[CONTRIBUTING]] — Standards for bug reporting, pull requests, testing with `pytest`, and code style.
* [[CODE_OF_CONDUCT]] — Community engagement standards and pledge.

### 2. Theoretical & Data Foundations
* [[docs/CORE_CONCEPTS]] — Zero-Day configuration, network topology representation, neuro-symbolic inference, and Medallion architecture.
* [[docs/SYSTEM_WORKFLOW]] — The deterministic 5-phase data transformation lifecycle.
* [[docs/DATA_MODELS]] — Complete specification of `KinematicMap`, Domain Entities, SQLite staging tables, and the unified Parquet schema.

### 3. Execution & Computation Engines
* [[docs/ETL_PIPELINE]] — Multi-threaded ingestion, `SensorBatchProcessor`, `ETLStorageRepository`, and concurrency tuning.
* [[docs/MATH_ENGINE]] — Polars AST compiler, computational graphs, unit conversions, and SI physical normalization.
* [[docs/NEURAL_PIPELINE]] — Phi-4-mini reasoning model, prompt builder, output parser, and neuro-symbolic resolver.
* [[docs/HARDWARE_AND_CUDA]] — CUDA dynamic library discovery, GPU VRAM offload, and hardware telemetry.

### 4. Operational Manual
* [[docs/USER_GUIDE]] — Step-by-step visual tutorial for loading maps, adding sensors, editing schema associations, and generating the final dataset.

---

*Return to [[README]]*
