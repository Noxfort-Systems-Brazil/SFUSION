# 🧪 Тестирование и обеспечение качества

Набор тестов SFusion включает **160 автоматизированных тестов** Pytest, обеспечивающих >91% покрытия кода во всех подсистемах: доменная модель, интерфейс (UI), контроллеры, конвейер ETL, расчеты в Polars и инференс SLM.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | ⚡ [Спецификация API](api_reference.md)

---

## 1. Запуск тестового набора

### 1.1 Запуск всех тестов в режиме headless
Используя локальное виртуальное окружение с PySide6 в фоновом режиме:
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 Генерация отчета о покрытии кода
Измерение покрытия для бэкенда (`src/`) и фронтенда (`ui/`):
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
Интерактивный HTML-отчет сохраняется в `htmlcov/index.html`. Общее покрытие SFusion превышает **91%** (Фронтенд: **~97%**, Бэкенд: **~89%**).

---

## 2. Структура тестов (160 тестов в 10 модулях)

| Модуль | Файл тестов | Тестируемый компонент | Проверяемое поведение |
| :--- | :--- | :--- | :--- |
| **Компоненты UI** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_main_window.py` | Виджеты Qt (`ui/`) | Offscreen-тестирование без X11/Wayland, раскладки, сигналы/слоты, выбор в списках, контекстные меню, зум/панорамирование (~97% покрытия). |
| **Контроллеры** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | Контроллеры (`src/controllers/`) | Координация 5 фаз конвейера (Persist -> ETL -> Parquet -> Cleanup), визуальное выделение дорог и синхронизация с AppState. |
| **Ядро и DI** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder и MapRenderer | Полное связывание зависимостей, векторная отрисовка в QGraphicsScene (полосы, узлы, стрелки) и валидация Pydantic. |
| **SLM и рассуждения** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | Модуль SLM (`src/slm/`) | Детерминированное сопоставление физических единиц, эвристический анализ схем, фильтрация тегов `<think>` и генерация промптов. |
| **Доменные модели** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Реактивные сигналы Qt (`map_data_loaded`, `data_sources_changed`), спаривание направлений дорог и инвариант `_is_savable()`. |
| **Подсистема ETL** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL и трансформаторы | Многопоточное извлечение, MD5-хеширование, zlib-сжатие, PRAGMA SQLite WAL, распаковка данных и расчеты в Polars. |
| **Сервисный слой** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Фоновые сервисы | Компиляция Polars AST, единицы СИ ($km/h$, $m/s$, $mph$), гармоническая скорость, экспорт Parquet, парсер SUMO XML/GZ и `.sfm.json`. |
| **Утилиты** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | Утилиты и оборудование | Сохранение конфигурации, вложенные переводы i18n, телеметрия CPU/VRAM, динамический поиск библиотек CUDA и fallback. |

---

## 3. Стратегия изоляции и моков

1. **Headless Offscreen платформа Qt**: Виджеты PySide6 тестируются без активного графического сервера с переменной `QT_QPA_PLATFORM=offscreen`. `tests/conftest.py` объявляет глобальную фикстуру `qapp` и моки для `i18n` и конфигурации.
2. **Детерминированные моки SLM**: Тесты `SLMEngine` и `NeuroSymbolicResolver` используют статические JSON-ответы, не требуя реального GPU или загрузки весов 3.5 ГБ.
3. **Изоляция SQLite WAL**: Тесты ETL используют временные базы SQLite с режимом WAL для проверки параллельной записи без записи постоянных файлов.
4. **Песочница временных файлов**: Все генерируемые файлы (`.sfm.json`, SQLite и Parquet) создаются внутри фикстуры pytest `tmp_path` и удаляются автоматически.
5. **Перехват завершения процесса**: Вызов `os._exit(0)` в `MainWindow.closeEvent` изолируется через `monkeypatch`, чтобы предотвратить сбой запуска pytest.

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Архитектура](architecture.md)
* [Спецификация API](api_reference.md)

