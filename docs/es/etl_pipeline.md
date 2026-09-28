# ⚡ Pipeline ETL de Alto Rendimiento

El **Pipeline ETL de SFusion** es un motor multihilo de alto rendimiento diseñado para procesar telemetría heterogénea masiva y transformarla en conjuntos cinemáticos unificados en formato Parquet.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 📐 [Motor de Física](math_engine.md)

---

## 1. Patrón Medallón en 3 Niveles

```mermaid
flowchart LR
    A["Datos Brutos"] --> B["SensorBatchProcessor (MD5, zlib)"]
    B --> C["NeuralTransformer + MathEngine (Polars)"]
    C --> D["ETLStorageRepository (SQLite WAL)"]
    D --> E["ParquetService (Dataset Oro Parquet)"]
```

1. **Capa Bronce**: Archivos brutos comprimidos con `zlib` (nivel 6) y protegidos con hash MD5 en `raw_data_storage`.
2. **Capa Plata**: Registros procesados con `orjson`, evaluados mediante expresiones de `MathEngine` e insertados en tablas `section_<fuente>`.
3. **Capa Oro**: Exportación colunar final en Apache Parquet con compresión Snappy.

---

## 2. Concurrencia y Afinación de SQLite WAL

El repositorio de almacenamiento implementa Write-Ahead Logging (WAL) de alto rendimiento:
```sql
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 120000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB de cache en RAM
PRAGMA temp_store = MEMORY;
```
Las transacciones por lote se ejecutan bajo protección de `threading.Lock()`, impidiendo errores de bloqueo entre hilos concurrentes.

---

## 3. Limpieza Automática de Archivos Temporales

Una vez concluida la exportación Parquet, `MainController._cleanup_temp_files()` elimina la base temporal `.temp_sfusion_<nombre>.db` y todos sus archivos asociados (`-wal`, `-shm`).

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Modelos de Datos](data_models.md)
* [Flujo de Trabajo](system_workflow.md)
