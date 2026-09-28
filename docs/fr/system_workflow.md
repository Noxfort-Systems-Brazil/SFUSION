# 🔄 Flux de Travail du Système et Cycle de Vie

Le processus complet de transformation des données s'exécute en 5 phases séquentielles :

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | 🖥️ [Guide Utilisateur](user_guide.md)

---

## 1. Les 5 Phases

1. **Ingestion de Réseau** : Chargement du fichier XML SUMO (`.net.xml` ou `.net.xml.gz`) et rendu vectoriel de la carte.
2. **Enregistrement des Sources** : Analyse des dossiers de capteurs et détection des extensions de fichiers.
3. **Association et Découverte** : Liaison des données à une voie (Local) ou à l'ensemble du réseau (Global) et analyse par Phi-4-mini.
4. **Staging ETL** : Traitement multithread vers la base SQLite WAL temporaire avec application de la physique vectorielle.
5. **Export Parquet et Nettoyage** : Consolidation finale en Apache Parquet Snappy et suppression des bases de travail temporaires.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Pipeline ETL](etl_pipeline.md)
* [Guide Utilisateur](user_guide.md)
