# SFusion Mapper

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework: PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-green.svg)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C.svg)](https://pola.rs/)
[![Format: Apache Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal.svg)](https://parquet.apache.org/)

**SFusion Mapper** is a high-performance, open-source Graphical User Interface (GUI) and data engineering application designed as the **"Day Zero" configuration and transformation engine** for the **SFusion ETL Ecosystem**.

It allows traffic engineers, data scientists, and simulation researchers to visually map arbitrary, heterogeneous urban sensor streams (Waze, TomTom, loop detectors, radar cameras) onto microscopic network topologies (such as SUMO). Powered by an embedded **Small Language Model (Phi-4-mini)** and a vectorized **Polars physics engine**, SFusion normalizes disparate units and exports consolidated, production-ready **Apache Parquet (`.parquet`)** datasets.

---

## ✨ Key Capabilities

* 🗺️ **SUMO Map Ingestion:** Loads microscopic road networks in both standard `.net.xml` and compressed `.net.xml.gz` formats.
* 📁 **Heterogeneous Sensor Support:** Ingests folders containing CSV, JSON, XML, and Excel telemetry datasets.
* 🧠 **Neuro-Symbolic Schema Discovery:** Leverages a local Small Language Model (Phi-4-mini-reasoning GGUF) to deduce semantic column mappings automatically, validated against deterministic physical heuristics.
* ⚡ **Vectorized Physics Compilation:** Uses Polars computational graphs (`pl.Expr`) to normalize speeds, flows, and intensities into standard SI / SUMO units ($km/h$, $veh/h$, $veh/km$) at memory-speed.
* 🛣️ **Intelligent Road Pairing:** Automatically identifies and groups opposing directional road pairs (e.g., `edge_12` and `-edge_12`) for consistent naming and simultaneous sensor association.
* 🌐 **Local & Global Mapping:** Binds sensor data either locally (to specific road segments or intersections) or globally (applying city-wide parameters).
* 💾 **Session Persistence:** Saves visual mapping sessions, customized street names, and associations into lightweight project files (`.sfm.json`).
* 📦 **Gold Columnar Export:** Compiles the final normalized traffic time-series into high-throughput **Apache Parquet (`.parquet`)** files.
* 🌍 **Internationalization (i18n):** Dual-layer translation engine supporting English, Portuguese (`pt_BR`), Spanish (`es`), French (`fr`), Russian (`ru`), and Mandarin (`zh`).

---

## 📚 Documentation & Knowledge Base (Obsidian Hub)

SFusion features a complete, interconnected knowledge base accessible both on GitHub and as an **Obsidian Vault**:

<div align="center">
  <table>
    <tr>
      <td align="center" width="25%">
        <h3>🏗️ <a href="ARCHITECTURE.md">Architecture</a></h3>
        <p>Clean MVC, Builder pattern, and layer specifications.</p>
        <p><i>[[ARCHITECTURE]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>📚 <a href="docs/INDEX.md">Docs Hub (MOC)</a></h3>
        <p>Central Map of Content connecting all guides.</p>
        <p><i>[[docs/INDEX]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>🧠 <a href="docs/NEURAL_PIPELINE.md">Neural & SLM</a></h3>
        <p>Phi-4-mini inference and neuro-symbolic resolver.</p>
        <p><i>[[docs/NEURAL_PIPELINE]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>⚡ <a href="docs/ETL_PIPELINE.md">ETL Pipeline</a></h3>
        <p>Multi-threaded ingestion and Parquet export.</p>
        <p><i>[[docs/ETL_PIPELINE]]</i></p>
      </td>
    </tr>
    <tr>
      <td align="center" width="25%">
        <h3>📐 <a href="docs/MATH_ENGINE.md">Math Engine</a></h3>
        <p>Polars AST compilation and SI unit normalization.</p>
        <p><i>[[docs/MATH_ENGINE]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>🗃️ <a href="docs/DATA_MODELS.md">Data Models</a></h3>
        <p>Entities, schemas, SQLite staging, and Parquet.</p>
        <p><i>[[docs/DATA_MODELS]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>🚀 <a href="docs/HARDWARE_AND_CUDA.md">Hardware / CUDA</a></h3>
        <p>GPU offload, dynamic loader, and telemetry.</p>
        <p><i>[[docs/HARDWARE_AND_CUDA]]</i></p>
      </td>
      <td align="center" width="25%">
        <h3>🖥️ <a href="docs/USER_GUIDE.md">User Guide</a></h3>
        <p>Step-by-step GUI tutorial and operations manual.</p>
        <p><i>[[docs/USER_GUIDE]]</i></p>
      </td>
    </tr>
  </table>
</div>

---

## 🚀 Getting Started

### Prerequisites

* **Operating System:** Linux (Ubuntu 20.04+, Debian 11+, Fedora, Arch) or Windows 10/11.
* **Python:** Version 3.9 or higher (Python 3.10 – 3.12 recommended).
* **System Libraries (Linux):**
  ```bash
  sudo apt update
  sudo apt install python3-venv build-essential libqt6gui6 libqt6widgets6 libgl1 libxcb-cursor0
  ```
* **Hardware Acceleration (Optional, Recommended):**
  * NVIDIA GPU with $\ge 6$ GB VRAM (RTX 3060 or higher).
  * NVIDIA Driver $\ge 525.60$ with CUDA 12.x support.
  * *Note: If no GPU is available, the system falls back automatically to multi-threaded CPU execution.*

---

### Local Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Noxfort-Labs/sfusion-mapper.git
   cd sfusion-mapper
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify the SLM Model:**
   The project expects the quantized model binary at:
   ```
   src/models/Phi-4-mini-reasoning-UD-Q6_K_XL.gguf
   ```
   *If the model file is not present, download it from the project releases or Hugging Face repository and place it into `src/models/`.*

5. **Run the Application:**
   ```bash
   python sfusion.py
   ```

---

## 🧪 Running Unit Tests

SFusion includes a comprehensive test suite covering domain entities, services, the Polars math engine, ETL workers, and CUDA loaders:

```bash
# Run all tests
pytest

# Run tests with detailed verbosity
pytest -v

# Run a specific test suite
pytest tests/test_services/test_math_engine.py
```

---


## 🤝 Contributing

Contributions are warmly welcomed! Please review our [[CONTRIBUTING|Contribution Guidelines]] and [[CODE_OF_CONDUCT|Code of Conduct]] prior to submitting pull requests.

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0 or later (AGPL-3.0-or-later)**. See the [LICENSE](LICENSE) file for full details.