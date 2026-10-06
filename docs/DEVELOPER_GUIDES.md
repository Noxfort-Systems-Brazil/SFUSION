---
tags: [developer, guide, setup, mvc, builder, polars, slm, testing]
aliases: [Developer Guides, Developer Reference, Contribution Guide]
---

# 🛠️ Developer & Integration Guides

This document provides step-by-step developer guidelines for setting up the development environment, understanding the Clean MVC architecture, extending sensor extractors, configuring Polars expressions, and running automated tests.

⬅️ Back to [Main Documentation Hub](SFUSION_MOC.md) | 🏛️ See [Architecture](ARCHITECTURE.md) | ⚡ See [ETL Pipeline](ETL_PIPELINE.md) | 🧪 See [Testing](TESTING.md)

---

## 1. Development Environment Setup

### 1.1 System Prerequisites
SFusion Mapper is built upon **Python 3.9+** and **PySide6 (Qt6)**. On Debian/Ubuntu Linux distributions, ensure system graphics and compilation packages are installed:

```bash
sudo apt update
sudo apt install -y \
    python3-venv \
    build-essential \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6dbus6 \
    libxkbcommon-x11-0 \
    libgl1 \
    libxcb-cursor0
```

### 1.2 Virtual Environment & Dependencies
Clone the repository and set up an isolated virtual environment:

```bash
git clone https://github.com/Noxfort-Systems-Brazil/SFUSION.git
cd SFUSION

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 1.3 Quantized SLM Model Setup
The neuro-symbolic inference engine requires the quantized **Phi-4-mini-reasoning GGUF** model placed inside `src/models/`:

```bash
# Model target path:
src/models/Phi-4-mini-reasoning-UD-Q6_K_XL.gguf
```

If testing without a GPU or model file, the system automatically falls back to deterministic heuristic heuristics via `NeuroSymbolicResolver`.

---

## 2. Architectural Guidelines & Clean MVC

SFusion strictly isolates responsibilities across architectural boundaries:

```text
View (ui/) <---> Controller (src/controllers/) <---> Model (src/domain/ & AppState)
                          │
                          ▼
              Services (src/services/ & src/etl/)
                          │
                          ▼
              SLM Subsystem (src/slm/)
```

### 2.1 Dependency Injection via `AppBuilder`
Never instantiate views and controllers directly with hard-coded cross-references. All components must be assembled via [`src/core/app_builder.py`](../src/core/app_builder.py):

```python
builder = AppBuilder()
builder.create_domain()
builder.create_services()
builder.create_controllers()
builder.create_views()
builder.wire_signals()
app_window = builder.build()
```

### 2.2 Thread Safety & Concurrency
- **UI Thread Safety:** The PySide6 GUI thread must never perform heavy file I/O, regex parsing, Polars AST compilation, or LLM inference.
- **Worker Threads:** Background operations must be dispatched through `QThreadPool` or dedicated `QThread` workers (e.g., `SensorBatchProcessor`, `ParquetExportWorker`).
- **Signal Handshake:** Background workers communicate progress, telemetry, and results back to controllers exclusively via Qt Signals.

---

## 3. Extending Sensor Ingestion (`src/services/extractors.py`)

To add support for a new telemetry sensor format:

1. Define a new extractor class inheriting from `BaseExtractor`.
2. Implement header discovery and chunked preview sampling:

```python
from src.services.extractors import BaseExtractor

class CustomSensorExtractor(BaseExtractor):
    def extract_headers(self, file_path: str) -> list[str]:
        # Parse schema keys / column headers
        ...
        
    def sample_records(self, file_path: str, limit: int = 10) -> list[dict]:
        # Return lightweight sample rows for SLM preview
        ...
```

3. Register the extractor in `DataImporter.register_extractor()` in [`src/services/data_importer.py`](../src/services/data_importer.py).

---

## 4. Vector Physics Compilation (`src/services/math_engine.py`)

Physical unit conversions are compiled into vectorized Polars expressions (`pl.Expr`) executed in parallel with SIMD instructions:

```python
import polars as pl

# Example: Converting raw km/h speed column to SI meters per second (m/s)
speed_expr = pl.col("raw_speed_kmh") * (1000.0 / 3600.0)

# Computing Space Mean Harmonic Speed
harmonic_speed = pl.count() / (1.0 / pl.col("speed_mps")).sum()
```

When modifying mathematical formulas, always run the math test suite:
```bash
pytest tests/test_services/test_math_engine.py -v
```

---

## 5. Automated Testing Guidelines

We enforce an automated test coverage standard of **$\ge 80\%$** across backend and frontend code (current suite: **160 tests, >91% coverage**).

### 5.1 Running Headless Tests
All tests must execute cleanly in headless environments (e.g., CI/CD or terminal-only servers) using the offscreen Qt platform:

```bash
# Run entire test suite
QT_QPA_PLATFORM=offscreen pytest

# Run with verbose reporting and durations
QT_QPA_PLATFORM=offscreen pytest -v --durations=10

# Generate full terminal coverage breakdown
QT_QPA_PLATFORM=offscreen pytest --cov=src --cov=ui --cov-report=term-missing
```

### 5.2 Test Structure
- `tests/test_ui/`: Headless PySide6 widget tests using `pytest-qt` and simulated user interactions.
- `tests/test_controllers/`: Signal propagation and mediator state updates.
- `tests/test_core/`: AppBuilder dependency wiring and MapRenderer vector calculations.
- `tests/test_domain/`: AppState state mutations and validation.
- `tests/test_etl/`: Sensor batch parsing, MD5 hashing, and SQLite WAL transactions.
- `tests/test_services/`: Polars physics computations and Parquet export.
- `tests/test_slm/`: Prompt formatting, reasoning tag isolation, and heuristic resolvers.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
