# 🔄 Flujo de Trabajo del Sistema y Ciclo de Vida

El proceso de transformación de datos en SFusion se ejecuta en 5 etapas secuenciales:

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | 🖥️ [Guía de Usuario](user_guide.md)

---

## 1. Fases del Flujo

1. **Ingesta de Red**: Carga del archivo XML de SUMO (`.net.xml` o `.net.xml.gz`) y renderizado vectorial de aristas y cruces.
2. **Registro de Fuentes**: Inspección de carpetas de sensores y detección de formatos.
3. **Asociación y Descubrimiento**: Asociación de sensores a vías (Local) o a la red (Global) e inferencia con Phi-4-mini.
4. **Staging ETL**: Procesamiento multihilo hacia base temporal SQLite WAL con aplicación de física vectorial.
5. **Exportación Parquet y Limpieza**: Consolidación en Apache Parquet Snappy y eliminación de archivos temporales.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Pipeline ETL](etl_pipeline.md)
* [Guía de Usuario](user_guide.md)
