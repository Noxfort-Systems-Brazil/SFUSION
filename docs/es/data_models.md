# 🗃️ Modelos de Datos y Esquemas

Este documento detalla el diccionario de datos formal de **SFusion Mapper**, incluyendo entidades de dominio, estado reactivo, esquema `KinematicMap` y la especificación de exportación en **Apache Parquet**.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitectura](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md)

---

## 1. Entidades de Dominio (`src/domain/entities.py`)

### `AssociationType` (Enum)
* `UNASSOCIATED`: Fuente cargada pero sin asociar a la red.
* `GLOBAL`: Aplica a toda la red vial simultáneamente.
* `LOCAL`: Vinculada a un segmento (`MapEdge`) o intersección (`MapNode`).

### `DataSource` (Dataclass)
```python
@dataclass
class DataSource:
    path: str                                # Ruta absoluta en disco
    name: str                                # Nombre visible
    file_types: list[str] = field(...)       # Tipos detectados (["CSV", "JSON"])
    id: str = field(...)                     # Identificador único (ej: "src_a1b2c3d4")
    parser_id: str | None = None             # ID de extractor asignado
    association_type: AssociationType = ...  # UNASSOCIATED, GLOBAL o LOCAL
    associated_element_id: str | None = None # ID de elemento SUMO objetivo
```

---

## 2. Estado Reactivo de la Aplicación (`src/domain/app_state.py`)

* Hereda de `QObject` y emite señales de actualización: `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed`.
* **Condición de Exportación (`_is_savable`)**: Requiere que la red esté cargada y todas las fuentes `LOCAL` estén asociadas.

---

## 3. Esquema Cinemático Pydantic (`src/core/schemas.py`)

```python
class KinematicMap(BaseModel):
    speed_col: Optional[str] = None          # Columna de velocidad
    flow_col: Optional[str] = None           # Columna de flujo/volumen
    intensity_col: Optional[str] = None      # Columna de congestión/intensidad
    distance_col: Optional[str] = None       # Columna de distancia (v = d / t)
    time_col: Optional[str] = None           # Columna de tiempo (v = d / t)
    occupancy_col: Optional[str] = None      # Ocupación del sensor
    speed_unit: Optional[str] = "km/h"       # "km/h", "m/s" o "mph"
    confidence_score: Optional[float] = None # Confianza del modelo [0.0 - 1.0]
```

---

## 4. Esquema Final en Apache Parquet (`.parquet`)

| Columna | Tipo Arrow | ¿Nulo? | Descripción |
| :--- | :--- | :---: | :--- |
| `event_timestamp` | `timestamp[ns, UTC]` | No | Marca de tiempo normalizada en UTC. |
| `sensor_id` | `string` | No | Identificador del dispositivo sensor. |
| `sumo_id` | `string` | Sí | ID de la arista o cruce SUMO (`None` en Global). |
| `location_text` | `string` | Sí | Nombre asignado a la calle o avenida. |
| `lat` | `float64` | Sí | Latitud WGS84. |
| `lon` | `float64` | Sí | Longitud WGS84. |
| `origin_type` | `string` | No | Alcance: `"LOCAL"` o `"GLOBAL"`. |
| `speed_val` | `Int64` | Sí | **Velocidad normalizada a km/h** (entero). |
| `flow_val` | `float64` | Sí | **Flujo vehicular en veh/h** (2 decimales). |
| `intensity_val` | `float64` | Sí | **Índice de congestión** (2 decimales). |
| `source_table` | `string` | No | Tabla interna de origen (`section_<nombre>`). |

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Motor de Física](math_engine.md)
* [Pipeline ETL](etl_pipeline.md)
