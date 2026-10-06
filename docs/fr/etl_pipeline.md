# ⚡ Pipeline ETL Haute Performance

Le **Pipeline ETL de SFusion** est un moteur d'ingestion multithread et économe en mémoire vive, conçu pour transformer des volumes massifs de données de capteurs en fichiers Parquet unifiés.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 📐 [Moteur Physique](math_engine.md)

---

## 1. Modèle Médaillon à Trois Niveaux

```mermaid
flowchart LR
    A["Données Brutes"] --> B["SensorBatchProcessor (MD5, zlib)"]
    B --> C["NeuralTransformer + MathEngine (Polars)"]
    C --> D["ETLStorageRepository (SQLite WAL)"]
    D --> E["ParquetService (Dataset Or Parquet)"]
```

1. **Couche Bronze** : Fichiers bruts compressés avec `zlib` (niveau 6) et horodatés dans `raw_data_storage`.
2. **Couche Argent** : Décodage `orjson`, évaluation des formules du `MathEngine` et insertion dans les tables `section_<source>`.
3. **Couche Or** : Consolidation et export final en Apache Parquet compressé en Snappy.

---

## 2. Gestion de la Concurrence SQLite WAL

Le dépôt de stockage configure le mode Write-Ahead Logging (WAL) :
```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 120000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64Mo de cache en mémoire
PRAGMA temp_store = MEMORY;
```
Les écritures par lot sont encapsulées dans un verrou atomique (`threading.Lock()`), éliminant les conflits d'écriture entre threads.

---

## 3. Suppression Automatique des Données Temporaires

Après l'export Parquet, `MainController._cleanup_temp_files()` supprime la base temporaire `.temp_sfusion_<nom>.db` et ses journaux associés (`-wal`, `-shm`).

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Modèles de Données](data_models.md)
* [Flux de Travail](system_workflow.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Sous licence AGPLv3.</small>
</div>
