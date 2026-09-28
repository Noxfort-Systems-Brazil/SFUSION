# 🗃️ Modelos de Dados e Esquemas

Este documento apresenta o dicionário de dados formal do **SFusion Mapper**, abrangendo entidades em memória, o estado reativo da aplicação, o blueprint cinemático Pydantic, o esquema SQLite de staging e a especificação unificada em **Apache Parquet**.

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md)

---

## 1. Entidades de Domínio (`src/domain/entities.py`)

### `AssociationType` (Enum)
* `UNASSOCIATED`: Fonte carregada, porém não vinculada à malha.
* `GLOBAL`: Telemetria aplicada uniformemente em toda a rede.
* `LOCAL`: Telemetria ancorada a um segmento viário (`MapEdge`) ou cruzamento (`MapNode`).

### `DataSource` (Dataclass)
```python
@dataclass
class DataSource:
    path: str                                # Caminho absoluto do diretório
    name: str                                # Nome amigável de exibição
    file_types: list[str] = field(...)       # Extensões detectadas (["CSV", "JSON"])
    id: str = field(...)                     # Identificador único (ex: "src_a1b2c3d4")
    parser_id: str | None = None             # ID do extrator correspondente
    association_type: AssociationType = ...  # UNASSOCIATED, GLOBAL ou LOCAL
    associated_element_id: str | None = None # ID da aresta ou nó SUMO associado
```

### `MapNode` e `MapEdge` (Dataclasses)
```python
@dataclass
class MapNode:
    id: str                                  # ID do cruzamento SUMO (ex: "J1")
    x: float                                 # Coordenada X na projeção da malha
    y: float                                 # Coordenada Y na projeção da malha
    node_type: str = "unknown"               # Tipo (traffic_light, priority, etc.)
    real_name: str | None = None             # Nome real da rua/cruzamento

@dataclass
class MapEdge:
    id: str                                  # ID da via SUMO (ex: "edge_42")
    from_node: str                           # Cruzamento de origem
    to_node: str                             # Cruzamento de destino
    shape: List[Tuple[float, float]] = ...   # Coordenadas da geometria da via
    real_name: str | None = None             # Nome real da avenida/rua
```

---

## 2. Estado Reativo da Aplicação (`src/domain/app_state.py`)

A classe `AppState` atua como **Fonte Única da Verdade (SSOT)** baseada em `QObject`:
* `map_data_loaded`: Disparado após parsing completo da rede SUMO.
* `data_sources_changed`: Emitido ao cadastrar ou excluir pastas de sensores.
* `data_association_changed`: Emitido ao vincular um sensor a uma via ou alternar para Global.
* `savable_state_changed`: Habilita ou desabilita o botão de geração do dataset.
* **Regra de Exportação (`_is_savable`)**: O dataset só pode ser gerado se: (1) houver mapa carregado e (2) todas as fontes marcadas como `LOCAL` estiverem associadas a elementos da malha.

---

## 3. Blueprint Cinemático Pydantic (`src/core/schemas.py`)

```python
class KinematicMap(BaseModel):
    # Colunas Cinemáticas Diretas
    speed_col: Optional[str] = None          # Coluna de velocidade
    flow_col: Optional[str] = None           # Coluna de vazão/volume
    intensity_col: Optional[str] = None      # Coluna de intensidade/congestionamento

    # Colunas para Derivação Cinemática (v = d / t)
    distance_col: Optional[str] = None       # Coluna de distância
    time_col: Optional[str] = None           # Coluna de duração/tempo
    occupancy_col: Optional[str] = None      # Ocupação do laço/sensor

    # Metadados de Unidades de Medida
    speed_unit: Optional[str] = "km/h"       # "km/h", "m/s", ou "mph"
    occupancy_unit: Optional[str] = None     # "ms", "s", ou "pct"
    distance_unit: Optional[str] = None      # "m", "km", ou "miles"
    time_unit: Optional[str] = None          # "s", "ms", "min", ou "hours"

    # Confiança da Inferência
    confidence_score: Optional[float] = None # Pontuação entre 0.0 e 1.0
```

---

## 4. Esquema Final em Apache Parquet (`.parquet`)

| Coluna | Tipo Arrow / Pandas | Nulo? | Descrição |
| :--- | :--- | :---: | :--- |
| `event_timestamp` | `timestamp[ns, UTC]` | Não | Timestamp do evento normalizado em UTC. |
| `sensor_id` | `string` | Não | Identificador do dispositivo sensor. |
| `sumo_id` | `string` | Sim | Identificador da via/nó SUMO (`None` para Global). |
| `location_text` | `string` | Sim | Nome real da rua configurado na interface. |
| `lat` | `float64` | Sim | Latitude WGS84 extraída do registro. |
| `lon` | `float64` | Sim | Longitude WGS84 extraída do registro. |
| `origin_type` | `string` | Não | Escopo do vínculo: `"LOCAL"` ou `"GLOBAL"`. |
| `speed_val` | `Int64` | Sim | **Velocidade convertida para km/h** (inteiro). |
| `flow_val` | `float64` | Sim | **Vazão de tráfego em veíc/h** (2 decimais). |
| `intensity_val` | `float64` | Sim | **Índice de intensidade/densidade** (2 decimais). |
| `source_table` | `string` | Não | Tabela de origem no staging (`section_<nome>`). |

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Motor Físico](math_engine.md)
* [Pipeline ETL](etl_pipeline.md)
