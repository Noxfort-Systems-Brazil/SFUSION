# 📖 Conceptos Fundamentales y Teoría

**SFusion Mapper** es la herramienta de ingeniería de datos "Day Zero" del ecosistema **SFusion ETL**. Su propósito fundamental es conectar telemetría de sensores urbanos heterogéneos y dispersos con simulaciones microscópicas de alta exigencia técnica (como SUMO).

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitectura](architecture.md) | 🔄 [Flujo de Trabajo](system_workflow.md)

---

## 1. El Paradigma "Day Zero"

Tradicionalmente, incorporar nuevos sensores urbanos requería programar scripts personalizados y expresiones regulares frágiles. Cualquier cambio en las cabeceras provocaba fallos en producción.

**SFusion Mapper elimina el ETL manual**:
* Funciona como una consola visual de preparación previa a la simulación ("Día Cero").
* El operador carga la red de carreteras y vincula fuentes interactivamente.
* La IA local (*Phi-4-mini*) deduce la semántica de las columnas con validación física matemática, exportando un archivo estándar de alto rendimiento en **Apache Parquet**.

---

## 2. Topología de Red y Asociación Espacial

Los datos de movilidad carecen de utilidad sin contexto geométrico:
* **Nodos (`MapNode`)**: Intersecciones y rotondas con coordenadas $(x, y)$.
* **Aristas (`MapEdge`)**: Vías direccionales con geometrías poligonales (`shape`).
* **Emparejamiento Inteligente de Vías**: Identificación y agrupación automática de sentidos contrarios (`edge_123` y `-edge_123`) para asignación unificada.
* **Asociación Local vs. Global**:
  * **Global**: Parámetros que aplican a toda la red (clima, límites generales de velocidad).
  * **Local**: Enlace directo a un tramo o cruce vial (radares, cámaras o espiras inductivas).

---

## 3. Descubrimiento Neuro-Simbólico de Esquemas

Diferentes fabricantes usan nombres dispares: `velocidad`, `spd_kmh`, `current_speed`.
* **Capa Neuronal**: El SLM local interpreta la intención semántica del dato.
* **Capa Simbólica**: El validador determinista (`NeuroSymbolicResolver`) restringe las salidas al contrato `KinematicMap`, verificando unidades de medida y previniendo alucinaciones.

---

## 4. Normalización Cinemática Vectorial

Las simulaciones demandan unidades físicas estandarizadas en el Sistema Internacional (SI / SUMO):
$$\text{Velocidad } (v) \in \text{km/h}, \quad \text{Flujo } (q) \in \text{veh/h}, \quad \text{Densidad } (k) \in \text{veh/km}$$

El `MathEngine` traduce el blueprint en un **Árbol Sintáctico Abstracto (AST)** en **Polars** (`pl.Expr`), procesando millones de registros en paralelo con aceleración SIMD.

---

## 5. Arquitectura Medallón

```mermaid
flowchart LR
    Bronce["🥉 Bronce (Bruto, MD5, zlib)"] --> Plata["🥈 Plata (Parsing orjson, SQLite WAL)"]
    Plata --> Oro["🥇 Oro (Apache Parquet Snappy)"]
```

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Modelos de Datos](data_models.md)
* [Motor de Física](math_engine.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingeniería de Movilidad Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado bajo AGPLv3.</small>
</div>
