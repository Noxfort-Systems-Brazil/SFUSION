<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — Suite de Documentación Técnica
### Arquitectura de Sistemas, Descubrimiento Neuronal y Física Vectorial
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Activo-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)

---

🌐 **Idiomas:** **[🇺🇸 English](../en/README.md)** • **[🇧🇷 Português (Brasil)](../pt-br/README.md)** • **[🇪🇸 Español](README.md)** • **[🇫🇷 Français](../fr/README.md)** • **[🇷🇺 Русский](../ru/README.md)** • **[🇨🇳 简体中文](../zh/README.md)** • **[📖 Centro de Documentación](../README.md)**

---

</div>

## Bienvenido a la Documentación Técnica Oficial

Este directorio reúne la suite completa de documentación técnica en **Español** para **SFusion Mapper** (SYNAPSE Fusion) — la herramienta visual de ingeniería de datos "Day Zero" y normalización cinemática desarrollada por Noxfort Systems. SFusion conecta flujos heterogéneos de sensores urbanos (Waze, TomTom, lazos inductivos, cámaras radar) con entornos de simulación microscópica de tráfico como SUMO.

## Índice de Guías Especializadas

| Documento | Alcance & Tema | Principales Tópicos |
| :--- | :--- | :--- |
| 🏛️ **[Arquitectura del Sistema](architecture.md)** | Especificación Técnica | Clean MVC, inyección de dependencias con patrón Builder, capa View en PySide6, servicios desacoplados y AppState reactivo como Fuente Única de Verdad. |
| 📖 **[Conceptos Fundamentales](core_concepts.md)** | Fundamentos Teóricos | Paradigma "Day Zero", topología de grafos de SUMO (MapNode/MapEdge), inferencia neuro-simbólica y arquitectura Medallón (Bronce/Plata/Oro). |
| 🗃️ **[Modelos de Datos y Esquemas](data_models.md)** | Diccionario de Datos | Entidades de dominio inmutables, contrato Pydantic v2 `KinematicMap`, base temporal SQLite WAL y esquema final unificado en Apache Parquet. |
| ⚡ **[Pipeline ETL de Alto Rendimiento](etl_pipeline.md)** | Motor de Ingesta | Orquestación multihilo con `QThreadPool`, `SensorBatchProcessor`, hash MD5, compresión zlib y afinación PRAGMA de SQLite WAL. |
| 📐 **[Motor de Física Vectorial](math_engine.md)** | Compilación AST en Polars | Transformaciones vectoriales SIMD sin contención de GIL, normalización SI ($km/h$, $m/s$, $mph$), velocidad media armónica y densidad $k = q / v$. |
| 🧠 **[Pipeline Neuronal (SLM)](neural_pipeline.md)** | Razonamiento de IA Local | Modelo cuántico local *Phi-4-mini* GGUF, runtime `llama.cpp`, extracción de jerarquías JSON, filtrado de `<think>` y `NeuroSymbolicResolver`. |
| 🚀 **[Aceleración por Hardware y CUDA](hardware_and_cuda.md)** | Infraestructura de GPU | Cargador dinámico de bibliotecas CUDA (`ensure_cuda_libs`), `slm_settings.json`, uso de TensorCores, fallback para CPU y telemetría de VRAM. |
| 🔄 **[Flujo de Trabajo del Sistema](system_workflow.md)** | Ciclo de Vida de Datos | Ejecución determinista de 5 fases: Ingesta de Red, Registro de Fuentes, Asociación y Descubrimiento, Staging ETL y Exportación a Parquet. |
| 🖥️ **[Guía de Usuario y Operaciones](user_guide.md)** | Manual del Operador | Navegación en lienzo (zoom/pan), emparejamiento bidireccional de vías, asociación local/global, anulación manual y proyectos `.sfm.json`. |
| 🧪 **[Pruebas y Aseguramiento de Calidad](testing.md)** | Estándares de QA | 160 pruebas automáticas con Pytest, cobertura >91% en backend y frontend, ejecución headless Qt, mocks de IA y división en 10 módulos. |
| ⚡ **[Referencia de la API Interna](api_reference.md)** | Contratos de Clases y Señales | Especificación técnica de modelos de dominio, servicios de background, repositorio DAO, señales Qt y controladores mediadores. |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingeniería de Movilidad Inteligente • SFusion Mapper v0.1.0</i>
</div>
