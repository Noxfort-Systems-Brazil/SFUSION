# 🧪 Directrices de Pruebas y Validación de Calidad

SFusion cuenta con **66 pruebas automáticas** en Pytest que cubren el 100% de los subsistemas de dominio, ETL, modelos físicos y análisis SLM.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | ⚡ [Referencia de API](api_reference.md)

---

## 1. Ejecución de Pruebas

```bash
./.venv/bin/pytest tests/ -v
```

Generación de reporte de cobertura:
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. Resumen de Módulos (66 Pruebas)

* `test_slm_engine.py`: Fachada del motor SLM.
* `test_main_controller.py`: Control del ciclo de vida y limpieza de staging.
* `test_schemas.py`: Validación de esquemas Pydantic.
* `test_app_state.py` y `test_entities.py`: Señales reactivas de Qt y modelos de dominio.
* `test_sensor_processor.py` y `test_storage_repository.py`: Ingesta ETL y base SQLite WAL.
* `test_math_engine.py` y `test_parquet_service.py`: Física en Polars y exportación Parquet.
* `test_slm_output_parser.py`: Filtrado de bloques `<think>`.
* `test_cuda_loader.py`: Detección dinâmica de bibliotecas de CUDA.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Arquitectura](architecture.md)
* [Referencia de API](api_reference.md)
