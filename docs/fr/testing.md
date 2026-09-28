# 🧪 Directives de Tests et Assurance Qualité

SFusion intègre **66 tests automatisés** sous Pytest validant la robustesse du domaine, de l'ETL, du moteur physique et du parsing IA.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [Référence API](api_reference.md)

---

## 1. Lancement des Tests

```bash
./.venv/bin/pytest tests/ -v
```

Rapport de couverture de code :
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. Découpage des 66 Tests

* `test_slm_engine.py` : Façade du moteur SLM.
* `test_main_controller.py` : Contrôle du cycle de vie et suppression des fichiers temporaires.
* `test_schemas.py` : Validation des schémas Pydantic.
* `test_app_state.py` et `test_entities.py` : Signaux réactifs Qt et modèles de domaine.
* `test_sensor_processor.py` et `test_storage_repository.py` : Ingestion ETL et persistance SQLite WAL.
* `test_math_engine.py` et `test_parquet_service.py` : Moteur Polars et export Parquet.
* `test_slm_output_parser.py` : Filtrage des balises `<think>`.
* `test_cuda_loader.py` : Détection dynamique de bibliothèques CUDA.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Architecture](architecture.md)
* [Référence API](api_reference.md)
