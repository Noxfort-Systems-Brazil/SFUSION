# 📐 Motor de Física Vectorial y Compilador AST

El **MathEngine** (`src/services/math_engine.py`) es el núcleo computacional para normalización física de tráfico en SFusion. Ejecuta enteramente en CPU y RAM utilizando expresiones vectoriales de **Polars**.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitetura](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md)

---

## 1. Normalización a Unidades SI

Simuladores como SUMO exigen unidades estándar:
* **Velocidad ($v$)**: $\text{km/h}$
* **Flujo ($q$)**: $\text{veh/h}$
* **Densidad ($k$)**: $\text{veh/km}$

---

## 2. Compilación AST (`compile_ast`)

Traduce el blueprint `KinematicMap` en expresiones de Polars:
* **Velocidad**:
  * `'m/s'`: $\text{velocidad} \times 3.6$
  * `'mph'`: $\text{velocidad} \times 1.60934$
  * `'knots'`: $\text{velocidad} \times 1.852$
  * Faltante: calculada mediante $\text{velocidad} = \frac{\text{distancia\_km}}{\text{tiempo\_horas}}$
* **Distancia**: Conversión de `'m'`, `'miles'` a kilómetros.
* **Tiempo**: Conversión de `'s'`, `'ms'`, `'min'` a horas.

---

## 3. Agregaciones Macroscópicas de Tráfico (`compile_aggregations`)

### 1. Velocidad Media Espacial (Media Armónica)
$$v_s = \frac{N}{\sum_{i=1}^{N} \frac{1}{v_i}}$$

### 2. Flujo Vehicular Macroscópico ($q$)
$$q = \frac{N}{\Delta t_{\text{horas}}} \quad [\text{veh/h}]$$

### 3. Densidad de Tráfico ($k$)
$$k = \frac{q}{v_s} \quad [\text{veh/km}]$$

---

## 4. Aritmética Segura
* **`safe_div`**: Sustituye denominadores de valor cero por `None`.
* **Casting sin errores**: Uso de `strict=False` para evitar caídas ante valores anómalos.
* **Filtro de infinitos**: Reemplazo de $\pm\infty$ por `np.nan`.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Pipeline Neuronal](neural_pipeline.md)
* [Modelos de Datos](data_models.md)
