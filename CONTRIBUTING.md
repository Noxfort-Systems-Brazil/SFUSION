# 🛠️ Contributing to SFusion Mapper

Thank you for your interest in contributing to **SFusion Mapper**! We welcome contributions from developers, researchers, traffic engineers, and open-source enthusiasts.

> [!NOTE]
> Please review our [[CODE_OF_CONDUCT]] before participating in our discussions and repository activities.

---

## 🚀 Development Environment Setup

1. **Fork and Clone the Repository:**
   ```bash
   git clone https://github.com/Noxfort-Labs/sfusion-mapper.git
   cd sfusion-mapper
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies in Editable Mode:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Your Setup:**
   Run the test suite to ensure all components and imports resolve correctly:
   ```bash
   pytest
   ```

---

## 🧪 Testing Standards

We maintain a high standard of reliability. All new features, bug fixes, and refactors must include corresponding unit tests in `tests/`:

* **Unit Tests**: Located under `tests/test_<layer>/` (e.g., `tests/test_services/`, `tests/test_etl/`, `tests/test_domain/`).
* **Running Tests:**
  ```bash
  # Run entire suite
  pytest

  # Run tests with output and execution times
  pytest -v --durations=10

  # Run a specific test module
  pytest tests/test_services/test_math_engine.py
  ```
* **Offline & Mocking Requirements**:
  Unit tests must not require a physical NVIDIA GPU or live download of the 3.5GB GGUF model. Use `unittest.mock` (such as `@patch('src.slm.llm_provider.Llama')`) to mock heavy external dependencies.

---

## 📐 Coding Guidelines & Architectural Principles

### 1. Strict MVC & Clean Architecture
* **Views (`ui/`)**: Must remain passive. Never write SQL queries, compute physics, or manipulate file systems directly in UI widgets. Views only emit Qt Signals and reflect model updates.
* **Controllers (`src/controllers/`)**: Mediate between views and domain models/services.
* **Domain Models (`src/domain/`)**: Serve as the Single Source of Truth (`AppState`). Keep state mutation observable via Qt Signals.
* **Services (`src/services/` & `src/etl/`)**: Handle computation (Polars), file parsing, database storage, and AI inference off the main GUI thread.

### 2. Internationalization (i18n)
* **Never hardcode user-facing strings or log messages**.
* For UI widgets: use `self._i18n.t("key")` backed by `locale/<lang>.json`.
* For backend services, workers, and domain logs: use `backend_i18n.t("key")` backed by `locale_backend/<lang>.json`.

### 3. Type Annotations & Schemas
* Use standard Python type hints (`typing.Optional`, `typing.List`, `typing.Dict`).
* Use **Pydantic v2** models for data interchange contracts (such as [[docs/DATA_MODELS#kinematic-schema|KinematicMap]]).

---

## 🔄 Pull Request Workflow

1. **Create a Feature Branch:**
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. **Implement Your Changes:**
   * Write clean, readable code adhering to PEP 8.
   * Preserve all existing comments and license headers.
   * Add or update unit tests.
3. **Update Documentation & Changelog:**
   * If you introduce new services or schemas, update the corresponding markdown documents in `docs/` and [[ARCHITECTURE]].
   * Document your changes under `## [Unreleased]` in [[CHANGELOG]].
4. **Run Verification:**
   ```bash
   pytest
   ```
5. **Submit the Pull Request:**
   * Provide a concise, clear description of the problem solved and changes made.
   * Reference any relevant GitHub issues.

---

## 🐛 Reporting Issues & Bugs

When reporting an issue, please provide:
1. Your OS distribution, Python version, and GPU model (if applicable).
2. Relevant excerpts from `sfusion.log` and `Sfusion_slm.log`.
3. Minimal reproducible steps or sample data header.

---

## 🔗 Related Documentation
* [[docs/INDEX]] - Knowledge Base Map of Content
* [[ARCHITECTURE]] - Technical Architecture
* [[CHANGELOG]] - Version History
* [[README]] - Project Overview
