# 📖 Concepts Fondamentaux et Théorie

**SFusion Mapper** constitue l'outil d'ingénierie des données « Jour Zéro » de l'écosystème **SFusion ETL**. Sa fonction première est de convertir les flux de capteurs urbains non standardisés en ensembles de données cinématiques rigoureusement calibrés pour les simulations microscopiques (telles que SUMO).

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🔄 [Flux de Travail](system_workflow.md)

---

## 1. Le Paradigme « Jour Zéro »

Dans l'ingénierie de données conventionnelle, le traitement de nouvelles sources de capteurs implique l'écriture de scripts dédiés et d'expressions régulières instables. Toute modification de format par un fournisseur de capteurs interrompt la chaîne de traitement.

**SFusion Mapper élimine l'ingénierie manuelle** :
* Console visuelle d'amorçage et de contrôle qualité avant simulation (« Jour Zéro »).
* Chargement graphique du réseau routier et liaison interactive des répertoires de données.
* Résolution automatique des schémas par un SLM local (*Phi-4-mini*) avec validation physique déterministe et export direct en **Apache Parquet**.

---

## 2. Topologie de Réseau et Ancrage Spatial

Les données de trafic exigent une référence géographique formelle :
* **Nœuds (`MapNode`)** : Intersections et carrefours munis de coordonnées $(x, y)$.
* **Tronçons (`MapEdge`)** : Voies orientées dotées de coordonnées géométriques (`shape`).
* **Appariement Intelligent des Voies** : Identification et liaison automatique des deux sens de circulation (`edge_123` et `-edge_123`).
* **Association Locale vs Globale** :
  * **Globale** : Données s'appliquant uniformément à tout le réseau (météo, vitesse limite générale).
  * **Locale** : Liaison spécifique à une voie ou un carrefour (boucle, radar de vitesse).

---

## 3. Découverte Neuro-Symbolique de Schémas

Face à la multiplicité des appellations (`speed`, `vitesse`, `v_kmh`, `current_speed`) :
* **Composant Neural** : Le SLM local analyse le contenu textuel brut et déduit l'intention sémantique.
* **Composant Symbolique** : Le résolveur (`NeuroSymbolicResolver`) vérifie les colonnes candidates contre les lois de la physique et garantit la conformité avec le blueprint `KinematicMap`.

---

## 4. Normalisation Cinématique Vectorielle

Les moteurs de simulation nécessitent des grandeurs dans le Système International (SI / SUMO) :
$$\text{Vitesse } (v) \in \text{km/h}, \quad \text{Débit } (q) \in \text{véh/h}, \quad \text{Densité } (k) \in \text{véh/km}$$

Le `MathEngine` transforme le schéma en un **Arbre Syntaxique Abstrait (AST)** de **Polars** (`pl.Expr`), calculé en parallèle avec vectorisation SIMD.

---

## 5. Architecture Médaillon

```mermaid
flowchart LR
    Bronze["🥉 Bronze (Fichiers bruts, MD5, zlib)"] --> Argent["🥈 Argent (Parsing orjson, SQLite WAL)"]
    Argent --> Or["🥇 Or (Dataset unifié Parquet Snappy)"]
```

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Modèles de Données](data_models.md)
* [Moteur Physique](math_engine.md)
