<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — Комплект технической документации
### Архитектура систем, нейросетевое распознавание схем и векторная физика
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Активен-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)

---

🌐 **Языки:** **[🇺🇸 English](../en/README.md)** • **[🇧🇷 Português (Brasil)](../pt-br/README.md)** • **[🇪🇸 Español](../es/README.md)** • **[🇫🇷 Français](../fr/README.md)** • **[🇷🇺 Русский](README.md)** • **[🇨🇳 简体中文](../zh/README.md)** • **[📖 Главный Хаб](../README.md)**

---

</div>

## Добро пожаловать в официальную техническую документацию

В данном каталоге собрана полная техническая документация на **русском языке** для программного комплекса **SFusion Mapper** (SYNAPSE Fusion) — визуального инструмента инженерии данных «нулевого дня» (Day Zero) и кинематической нормализации, разработанного компанией Noxfort Systems. SFusion объединяет разнородные телеметрические потоки дорожных датчиков (Waze, TomTom, индуктивные петли, радары) с высокоточными микроскопическими средами имитационного моделирования (такими как SUMO).

## Предметный указатель руководств

| Руководство | Направление и область | Основные темы |
| :--- | :--- | :--- |
| 🏛️ **[Архитектура системы](architecture.md)** | Спецификация архитектуры | Модель Clean MVC, внедрение зависимостей через паттерн Builder, слой View на PySide6, фоновые сервисы и реактивный AppState как единый источник истины. |
| 📖 **[Базовые концепции](core_concepts.md)** | Теоретические основы | Парадигма «нулевого дня» (Day Zero), графовая топология SUMO (MapNode/MapEdge), нейро-символический вывод и медальонная архитектура (Bronze/Silver/Gold). |
| 🗃️ **[Модели данных и схемы](data_models.md)** | Справочник схем | Неизменяемые сущности предметной области, Pydantic v2 контракт `KinematicMap`, промежуточные таблицы SQLite WAL и единая схема Apache Parquet. |
| ⚡ **[Высокопроизводительный ETL](etl_pipeline.md)** | Конвейер загрузки | Многопоточная оркестрация через `QThreadPool`, `SensorBatchProcessor`, хэширование MD5, сжатие zlib и PRAGMA-настройка SQLite WAL. |
| 📐 **[Векторный физический движок](math_engine.md)** | Компиляция Polars AST | SIMD-векторизация без блокировок Python GIL, стандартизация единиц СИ ($km/h$, $m/s$, $mph$), гармоническая средняя скорость и плотность $k = q / v$. |
| 🧠 **[Нейросетевой конвейер (SLM)](neural_pipeline.md)** | Локальный ИИ-инференс | Локальная квантованная модель *Phi-4-mini* GGUF, среда `llama.cpp`, извлечение иерархий JSON, фильтрация тегов `<think>` и `NeuroSymbolicResolver`. |
| 🚀 **[Аппаратное ускорение и CUDA](hardware_and_cuda.md)** | Вычисления на GPU | Динамический загрузчик библиотек CUDA (`ensure_cuda_libs`), `slm_settings.json`, использование TensorCore, резервный режим CPU и телеметрия. |
| 🔄 **[Рабочий процесс системы](system_workflow.md)** | Жизненный цикл данных | Детерминированное 5-фазное выполнение: импорт топологии, регистрация датчиков, привязка и анализ, ETL-стадирование и экспорт в Parquet. |
| 🖥️ **[Руководство оператора](user_guide.md)** | Инструкция по GUI | Интерактивная навигация по карте (масштабирование/панорамирование), спаривание встречных полос, локальная/глобальная привязка и проекты `.sfm.json`. |
| 🧪 **[Тестирование и контроль качества](testing.md)** | Стандарты QA | 169 автоматизированных тестов Pytest, покрытие >91% бэкенда и фронтенда, запуск headless Qt, моки ИИ и разделение на 10 модулей. |
| ⚡ **[Спецификация внутреннего API](api_reference.md)** | Интерфейсы и сигналы | Техническое описание доменных сущностей, фоновых сервисов, паттерна DAO/Repository, сигналов Qt и контроллеров. |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Инженерия интеллектуальной мобильности • SFusion Mapper v0.1.0</i>
</div>
