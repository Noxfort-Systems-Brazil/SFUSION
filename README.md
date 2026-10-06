---
tags: [readme, home, sfusion]
aliases: [Projeto SFUSION, Root]
---

<div align="center">

<img src="docs/assets/sfusion-logo.png" alt="SFUSION Mapper Logo" width="130" />

# SFUSION MAPPER
### "Day Zero" ETL Configuration & Kinematic Normalization Tool
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat&logo=polars&logoColor=white)](https://pola.rs/)
[![Parquet](https://img.shields.io/badge/Output-Apache_Parquet-008080?style=flat&logo=apache&logoColor=white)](https://parquet.apache.org/)
[![License](https://img.shields.io/badge/License-AGPL_v3-blue?style=flat)](LICENSE)

[![SFUSION GitHub Repository Card](https://github-readme-stats.vercel.app/api/pin/?username=Noxfort-Systems-Brazil&repo=SFUSION&theme=dark)](https://github.com/Noxfort-Systems-Brazil/SFUSION)

---

🌐 **Translations / Idiomas:** **[🇺🇸 English](README.md)** • **[🇧🇷 Português do Brasil](docs/pt-br/README.md)** • **[🇪🇸 Español](docs/es/README.md)** • **[🇫🇷 Français](docs/fr/README.md)** • **[🇷🇺 Русский](docs/ru/README.md)** • **[🇨🇳 简体中文](docs/zh/README.md)** • **[📚 Documentation Hub](docs/README.md)**

---

</div>

**SFusion Mapper** is a high-performance Graphical User Interface (GUI) and data engineering application designed as the **"Day Zero" configuration and transformation engine** for the Noxfort smart mobility ecosystem. 

It enables traffic engineers, simulation researchers, and urban operators to visually map arbitrary, heterogeneous sensor feeds (Waze, TomTom, inductive loops, radar cameras) onto microscopic network topologies (SUMO `.net.xml`). Powered by an embedded local Small Language Model (**Phi-4-mini**) and a vectorized **Polars physics engine**, SFusion normalizes disparate units and exports consolidated, production-ready **Apache Parquet (`.parquet`)** datasets.

---

## 📚 Documentation Hub & Knowledge Vault

Explore the full architecture, internal mechanics, and developer guides for the SFUSION ecosystem:

| Card / Subsystem | Focus Area | Direct Link |
| :--- | :--- | :---: |
| 📚 **Documentation Hub** | Central Index & Navigation for all technical docs | [Explore Hub](docs/SFUSION_MOC.md) |
| 🏛️ **System Architecture** | Clean MVC, Builder Pattern, Service Layer & Concurrency | [View Blueprint](ARCHITECTURE.md) |
| 📖 **Core Concepts** | "Day Zero" Paradigm, SUMO Graph & Medallion Architecture | [View Concepts](docs/CORE_CONCEPTS.md) |
| 🗃️ **Data Models & Schemas** | Domain Entities, KinematicMap Blueprint & Parquet Specs | [View Schemas](docs/DATA_MODELS.md) |
| ⚡ **High-Performance ETL** | Multi-threaded Sensor Ingestion & SQLite WAL Staging | [View ETL](docs/ETL_PIPELINE.md) |
| 📐 **Vector Physics Engine** | Polars AST Compilation, SI Units & Harmonic Mean Speed | [View Math Engine](docs/MATH_ENGINE.md) |
| 🧠 **Neural Pipeline (SLM)** | Phi-4-mini reasoning model, llama.cpp & Neuro-Symbolic Resolver | [View Neural](docs/NEURAL_PIPELINE.md) |
| 🚀 **Hardware & CUDA** | GPU VRAM Offload, Dynamic Library Loader & Telemetry | [View Hardware](docs/HARDWARE_AND_CUDA.md) |
| 🔄 **System Workflow** | 5-Phase End-to-End Data Transformation Lifecycle | [View Workflow](docs/SYSTEM_WORKFLOW.md) |
| 🖥️ **User Guide & Operations** | Step-by-Step Interactive GUI Manual | [View User Guide](docs/USER_GUIDE.md) |
| 🛠️ **Developer Guides** | Environment Setup, Sensor Parsers & Coding Standards | [View Guides](docs/DEVELOPER_GUIDES.md) |
| 📦 **Deployment & Packaging** | PyInstaller Compilation (`sfusion.spec`), Docker & Packages | [View Packaging](docs/DEPLOYMENT_AND_PACKAGING.md) |
| 🧪 **Testing & QA** | 160 Pytest Automated Tests (>91% Coverage), Headless Qt & Mocks | [View Guidelines](docs/TESTING.md) |
| ⚡ **Internal API Reference** | Core Classes, Qt Signals, Methods & Contracts | [View API Reference](docs/API_REFERENCE.md) |

---

## ⚡ Core Architecture

- **Clean MVC & Dependency Injection:** Fully decoupled architecture orchestrated by [`AppBuilder`](src/core/app_builder.py), separating PySide6 UI views from backend controllers, domain entities, and background workers.
- **Neuro-Symbolic Schema Discovery:** Local offline SLM (Phi-4-mini via `llama.cpp`) combined with deterministic heuristic validators (`NeuroSymbolicResolver`) to deduce semantic sensor column mappings automatically.
- **Polars Vectorized Physics Compilation:** High-throughput SIMD expressions (`pl.Expr`) compiling speed ($km/h$), distance ($km$), flow ($veh/h$), and harmonic mean speeds without Python GIL bottlenecks.
- **Two-Tier Staging & Gold Storage:** Non-blocking SQLite WAL temporary transactions with MD5 batch hashing and zlib compression, exporting final consolidated datasets to columnar **Apache Parquet (`.parquet`)**.
- **Dynamic NVIDIA CUDA Loader:** Runtime discovery of native CUDA runtime libraries (`libcudart.so`, `libcublas.so`) with transparent CPU fallback and GPU telemetry.
- **Dual Internationalization (i18n):** Decoupled multi-language engine supporting UI widgets (`locale/`) and backend worker telemetry (`locale_backend/`) across 6 languages.

---

## 🚀 Quick Start

### 1. Requirements
Ensure you have Python 3.9+ (Python 3.10–3.12 recommended) and necessary Qt6 system libraries:
```bash
sudo apt update
sudo apt install -y python3-venv build-essential libqt6gui6 libqt6widgets6 libgl1 libxcb-cursor0
```

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Noxfort-Systems-Brazil/SFUSION.git
cd SFUSION

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Running the Ecosystem
```bash
# Using the startup script:
./run.sh

# Or directly via Python:
python sfusion.py
```

---

## 🧪 Testing & Validation

Run the offline automated test suite (160 tests, >91% coverage):
```bash
QT_QPA_PLATFORM=offscreen pytest -v --cov=src --cov=ui
```

---

<div align="center">
  <img src="docs/assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="48" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>Licensed under the <a href="LICENSE">GNU Affero General Public License v3.0</a>. © 2026 Noxfort Systems.</small>
</div>