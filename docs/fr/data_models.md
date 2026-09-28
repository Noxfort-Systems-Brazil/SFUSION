# 🗃️ Modèles de Données et Schémas

Ce document détaille le dictionnaire des données de **SFusion Mapper**, couvrant les entités en mémoire, l'état réactif, le schéma Pydantic `KinematicMap` et l'exportation colonnaire en **Apache Parquet**.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md)

---

## 1. Entités de Domaine (`src/domain/entities.py`)

### `AssociationType` (Énumération)
* `UNASSOCIATED` : Source chargée mais non reliée au réseau.
* `GLOBAL` : Paramètres appliqués à l'ensemble du réseau.
* `LOCAL` : Données ancrées à un tronçon (`MapEdge`) ou un carrefour (`MapNode`).

### `DataSource` (Dataclass)
```python
@dataclass
class DataSource:
    path: str                                # Chemin d'accès absolu
    name: str                                # Libellé d'affichage
    file_types: list[str] = field(...)       # Formats détectés (["CSV", "JSON"])
    id: str = field(...)                     # Identifiant unique (ex: "src_a1b2c3d4")
    parser_id: str | None = None             # ID de l'extracteur
    association_type: AssociationType = ...  # UNASSOCIATED, GLOBAL ou LOCAL
    associated_element_id: str | None = None # ID de l'élément SUMO cible
```

---

## 2. État Réactif de l'Application (`src/domain/app_state.py`)

* Dérivé de `QObject`, il émet les signaux d'interface : `map_data_loaded`, `data_sources_changed`, `data_association_changed`, `savable_state_changed`.
* **Règle d'Exportation (`_is_savable`)** : L'export n'est autorisé que si le réseau est chargé et que toutes les sources `LOCAL` sont associées.

---

## 3. Blueprint Cinématique Pydantic (`src/core/schemas.py`)

```python
class KinematicMap(BaseModel):
    speed_col: Optional[str] = None          # Colonne de vitesse
    flow_col: Optional[str] = None           # Colonne de débit / volume
    intensity_col: Optional[str] = None      # Colonne de congestion / intensité
    distance_col: Optional[str] = None       # Colonne de distance (v = d / t)
    time_col: Optional[str] = None           # Colonne de temps (v = d / t)
    occupancy_col: Optional[str] = None      # Taux d'occupation
    speed_unit: Optional[str] = "km/h"       # "km/h", "m/s" ou "mph"
    confidence_score: Optional[float] = None # Indice de confiance [0.0 - 1.0]
```

---

## 4. Schéma Final en Apache Parquet (`.parquet`)

| Colonne | Type Arrow | Nullable | Description |
| :--- | :--- | :---: | :--- |
| `event_timestamp` | `timestamp[ns, UTC]` | Non | Horodatage normalisé en UTC. |
| `sensor_id` | `string` | Non | Identifiant de l'appareil capteur. |
| `sumo_id` | `string` | Oui | Identifiant de voie/nœud SUMO (`None` en Global). |
| `location_text` | `string` | Oui | Nom de rue attribué dans l'interface. |
| `lat` | `float64` | Oui | Latitude WGS84 extraite. |
| `lon` | `float64` | Oui | Longitude WGS84 extraite. |
| `origin_type` | `string` | Non | Portée : `"LOCAL"` ou `"GLOBAL"`. |
| `speed_val` | `Int64` | Oui | **Vitesse normalisée en km/h** (entier). |
| `flow_val` | `float64` | Oui | **Débit horaire en véh/h** (2 décimales). |
| `intensity_val` | `float64` | Oui | **Indice de congestion** (2 décimales). |
| `source_table` | `string` | Non | Table source temporaire (`section_<nom>`). |

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Moteur Physique](math_engine.md)
* [Pipeline ETL](etl_pipeline.md)
