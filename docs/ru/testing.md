# 🧪 Тестирование и обеспечение качества

Набор тестов SFusion включает **66 автоматизированных тестов** Pytest, покрывающих доменную модель, ETL, расчеты в Polars и инференс SLM.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | ⚡ [Спецификация API](api_reference.md)

---

## 1. Запуск тестового набора

```bash
./.venv/bin/pytest tests/ -v
```

Генерация отчета о покрытии кода:
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. Структура тестов (66 тестов)

* `test_slm_engine.py`: фасад модуля SLM.
* `test_main_controller.py`: жизненный цикл и очистка файлов.
* `test_schemas.py`: валидация схем Pydantic.
* `test_app_state.py` и `test_entities.py`: реактивные сигналы Qt и сущности.
* `test_sensor_processor.py` и `test_storage_repository.py`: конвейер ETL и SQLite WAL.
* `test_math_engine.py` и `test_parquet_service.py`: формулы Polars и экспорт Parquet.
* `test_slm_output_parser.py`: фильтрация рассуждений `<think>`.
* `test_cuda_loader.py`: поиск библиотек CUDA.

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Архитектура](architecture.md)
* [Спецификация API](api_reference.md)
