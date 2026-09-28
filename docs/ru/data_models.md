# 🗃️ Модели данных и спецификации схем

В данном документе описываются внутренние структуры данных **SFusion Mapper**: объекты доменного слоя, реактивное состояние, модель `KinematicMap` и спецификация формата **Apache Parquet**.

⬅️ [Главный Хаб](README.md) | 🏛️ [Архитектура](architecture.md) | ⚡ [Конвейер ETL](etl_pipeline.md)

---

## 1. Сущности предметной области (`src/domain/entities.py`)

### `AssociationType` (Enum)
* `UNASSOCIATED`: источник загружен, но не привязан к графу.
* `GLOBAL`: параметры действуют на всю транспортную сеть.
* `LOCAL`: телеметрия привязана к ребру (`MapEdge`) или перекрестку (`MapNode`).

### `DataSource` (Dataclass)
```python
@dataclass
class DataSource:
    path: str                                # Абсолютный путь к каталогу
    name: str                                # Отображаемое имя
    file_types: list[str] = field(...)       # Обнаруженные типы (["CSV", "JSON"])
    id: str = field(...)                     # Уникальный идентификатор
    parser_id: str | None = None             # ID назначенного экстрактора
    association_type: AssociationType = ...  # UNASSOCIATED, GLOBAL или LOCAL
    associated_element_id: str | None = None # ID элемента SUMO
```

---

## 2. Реактивное состояние приложения (`src/domain/app_state.py`)

* Базируется на `QObject` и передает сигналы: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed`.
* **Условие экспорта (`_is_savable`)**: экспорт разрешен только при наличии загруженной карты и привязке всех `LOCAL` источников.

---

## 3. Кинематический контракт Pydantic (`src/core/schemas.py`)

```python
class KinematicMap(BaseModel):
    speed_col: Optional[str] = None          # Поле скорости
    flow_col: Optional[str] = None           # Поле интенсивности/потока
    intensity_col: Optional[str] = None      # Поле плотности/затора
    distance_col: Optional[str] = None       # Поле расстояния (v = d / t)
    time_col: Optional[str] = None           # Поле времени (v = d / t)
    occupancy_col: Optional[str] = None      # Занятость детектора
    speed_unit: Optional[str] = "km/h"       # "km/h", "m/s" или "mph"
    confidence_score: Optional[float] = None # Уверенность модели [0.0 - 1.0]
```

---

## 4. Схема результирующего файла Parquet (`.parquet`)

| Поле | Тип данных | Nullable | Описание |
| :--- | :--- | :---: | :--- |
| `event_timestamp` | `timestamp[ns, UTC]` | Нет | Метка времени события в UTC. |
| `sensor_id` | `string` | Нет | Идентификатор прибора или потока. |
| `sumo_id` | `string` | Да | ID ребра или узла в сети SUMO. |
| `location_text` | `string` | Да | Название улицы, заданное оператором. |
| `lat` | `float64` | Да | Широта WGS84. |
| `lon` | `float64` | Да | Долгота WGS84. |
| `origin_type` | `string` | Нет | Тип привязки: `"LOCAL"` или `"GLOBAL"`. |
| `speed_val` | `Int64` | Да | **Скорость в км/ч** (целое число). |
| `flow_val` | `float64` | Да | **Интенсивность потока в авт/ч**. |
| `intensity_val` | `float64` | Да | **Индекс затора/плотности**. |
| `source_table` | `string` | Нет | Название промежуточной таблицы. |

---

## 🔗 Полезные ссылки
* [Главный Хаб](README.md)
* [Физический движок](math_engine.md)
* [Конвейер ETL](etl_pipeline.md)
