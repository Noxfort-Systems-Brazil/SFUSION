# 📐 Moteur de Physique Vectorielle et Compilateur AST

Le **MathEngine** (`src/services/math_engine.py`) est le cœur de calcul cinématique de SFusion. Il s'exécute sur CPU et RAM au moyen d'expressions vectorisées en **Polars**.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md)

---

## 1. Normalisation en Unités SI

Le moteur normalise les données pour SUMO :
* **Vitesse ($v$)** : $\text{km/h}$
* **Débit ($q$)** : $\text{véh/h}$
* **Densité ($k$)** : $\text{véh/km}$

---

## 2. Compilation AST (`compile_ast`)

Transforme le schéma `KinematicMap` en expressions Polars :
* **Vitesse** :
  * `'m/s'` : $\text{vitesse} \times 3.6$
  * `'mph'` : $\text{vitesse} \times 1.60934$
  * Manquante : calculée via $\text{vitesse} = \frac{\text{distance\_km}}{\text{temps\_heures}}$
* **Distance** : conversion de `'m'`, `'miles'` en kilomètres.
* **Temps** : conversion de `'s'`, `'ms'`, `'min'` en heures.

---

## 3. Agrégations Macroscopiques de Trafic (`compile_aggregations`)

### 1. Vitesse Moyenne Spatiale (Moyenne Harmonique)
$$v_s = \frac{N}{\sum_{i=1}^{N} \frac{1}{v_i}}$$

### 2. Débit Horaire Macroscopique ($q$)
$$q = \frac{N}{\Delta t_{\text{heures}}} \quad [\text{véh/h}]$$

### 3. Densité de Trafic ($k$)
$$k = \frac{q}{v_s} \quad [\text{véh/km}]$$

---

## 4. Arithmétique Sécurisée
* **`safe_div`** : Remplace les dénominateurs nuls par `None`.
* **Casting permissif** : Utilisation de `strict=False` pour prévenir les crashs sur données corrompues.
* **Gestion des infinis** : Remplacement des valeurs $\pm\infty$ par `np.nan`.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Pipeline Neural](neural_pipeline.md)
* [Modèles de Données](data_models.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Sous licence AGPLv3.</small>
</div>
