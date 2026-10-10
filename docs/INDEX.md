---
tags: [moc, hub, docs, obsidian, sfusion, index]
aliases: [SFUSION Index, Knowledge Base Index, MOC Hub]
---

# 📚 SFusion Knowledge Base (MOC)

Welcome to the central **Map of Content (MOC)** for **SFusion Mapper**. This knowledge base organizes the conceptual, mathematical, architectural, and operational documentation of the ecosystem. All documents are interconnected using dual **Obsidian-style Wikilinks** and **GitHub-compatible Markdown links** for seamless graph visualization and web browsing.

For an exhaustive directory tree and technical breakdown, please visit the primary [Master Documentation Hub (SFUSION_MOC)](SFUSION_MOC.md).

---

## 🧭 Navigation Hub

| Section | Description | Key Documents |
| :--- | :--- | :--- |
| **🚀 Project Foundation** | Project overview, quick start, architecture, and standards | [[README|Project Overview]] • [[ARCHITECTURE|Technical Architecture]] • [[CHANGELOG|Version History]] • [[CONTRIBUTING|Contribution Guide]] • [[CODE_OF_CONDUCT|Code of Conduct]] • [[SECURITY|Security Policy]] |
| **📖 Core Concepts & Data** | Fundamental ideas, state management, and schema blueprints | [[CORE_CONCEPTS|Core Concepts]] • [[SYSTEM_WORKFLOW|System Workflow]] • [[DATA_MODELS|Data Models & Schemas]] |
| **⚡ Processing Engines** | High-performance ETL, vector compilation, and AI inference | [[ETL_PIPELINE|ETL Pipeline]] • [[MATH_ENGINE|Vector Physics Engine]] • [[NEURAL_PIPELINE|Neural Pipeline & SLM]] • [[HARDWARE_AND_CUDA|Hardware & CUDA]] |
| **🖥️ Guides & Operations** | Operational manual for GUI usage and developer workflows | [[USER_GUIDE|User Guide]] • [[DEVELOPER_GUIDES|Developer Guides]] • [[DEPLOYMENT_AND_PACKAGING|Deployment & Packaging]] |
| **🧪 QA & APIs** | Automated test suite, testing guidelines, and API reference | [[TESTING|Testing & QA]] • [[API_REFERENCE|API Reference]] |
| **🌐 Multi-Language Hub** | Documentation in 6 international languages | [[README|Language Selector (en, pt-br, es, fr, ru, zh)]] |

---

## 🗺️ Detailed Document Directory

### 1. Foundation & Architecture
* [Master MOC](SFUSION_MOC.md) — Comprehensive technical master documentation hub and directory tree.
* [Project Overview](../README.md) — High-level introduction, key features, prerequisites, and getting started.
* [Technical Architecture](ARCHITECTURE.md) — Model-View-Controller (MVC), Builder pattern, dependency injection, and layer separation.
* [Security Policy](../SECURITY.md) — Responsible vulnerability reporting and data integrity policy.
* [Version History](../CHANGELOG.md) — Semantic versioning tracking additions, optimizations, and breaking changes.
* [Contribution Guide](../CONTRIBUTING.md) — Standards for bug reporting, pull requests, testing with `pytest`, and code style.
* [Code of Conduct](../CODE_OF_CONDUCT.md) — Community engagement standards and pledge.

### 2. Theoretical & Data Foundations
* [Core Concepts](CORE_CONCEPTS.md) — Day Zero configuration, network topology representation, neuro-symbolic inference, and Medallion architecture.
* [System Workflow](SYSTEM_WORKFLOW.md) — The deterministic 5-phase data transformation lifecycle.
* [Data Models & Schemas](DATA_MODELS.md) — Complete specification of `KinematicMap`, Domain Entities, SQLite staging tables, and the unified Parquet schema.

### 3. Execution & Computation Engines
* [ETL Pipeline](ETL_PIPELINE.md) — Multi-threaded ingestion, `SensorBatchProcessor`, `ETLStorageRepository`, and concurrency tuning.
* [Vector Physics Engine](MATH_ENGINE.md) — Polars AST compiler, computational graphs, unit conversions, and SI physical normalization.
* [Neural Pipeline & SLM](NEURAL_PIPELINE.md) — Phi-4-mini reasoning model, prompt builder, output parser, and neuro-symbolic resolver.
* [Hardware & CUDA](HARDWARE_AND_CUDA.md) — CUDA dynamic library discovery, GPU VRAM offload, and hardware telemetry.

### 4. Operations, Quality Assurance & APIs
* [User Guide](USER_GUIDE.md) — Step-by-step visual tutorial for loading maps, adding sensors, editing schema associations, and generating the final dataset.
* [Developer Guides](DEVELOPER_GUIDES.md) — Comprehensive developer setup, extensibility rules, and architecture principles.
* [Deployment & Packaging](DEPLOYMENT_AND_PACKAGING.md) — PyInstaller binary compilation, Docker multi-stage builds, and desktop integration.
* [Testing & QA](TESTING.md) — Test suite structure (169 tests, >91% coverage), headless Qt execution, mocking strategy, and code coverage.
* [Internal API Reference](API_REFERENCE.md) — Technical specification of domain state, services, and controller classes.
* [Multi-Language Hub](README.md) — Central Multi-Language Hub and international navigation.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
