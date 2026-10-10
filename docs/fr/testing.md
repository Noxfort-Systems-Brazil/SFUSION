# 🧪 Directives de Tests et Assurance Qualité

SFusion intègre **169 tests automatisés** sous Pytest garantissant >91% de couverture globale sur le domaine, l'interface graphique (UI), les contrôleurs, l'ETL, le moteur physique et le parsing IA.

⬅️ [Hub de Documentation](README.md) | 🏛️ [Architecture](architecture.md) | ⚡ [Référence API](api_reference.md)

---

## 1. Lancement des Tests

### 1.1 Exécuter Tous les Tests Automatisés
En utilisant l'environnement virtuel avec PySide6 en mode sans tête (offscreen) :
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 Rapport de Couverture de Code
Pour mesurer la couverture de code du backend (`src/`) et du frontend (`ui/`) :
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
Le rapport HTML interactif sera généré dans `htmlcov/index.html`. SFusion maintient **>91% de couverture globale** (Frontend: **~97%**, Backend: **~89%**).

---

## 2. Découpage des 169 Tests (10 Modules)

| Module de Test | Fichier de Test | Composant Ciblé | Comportements Validés |
| :--- | :--- | :--- | :--- |
| **Vues Frontend (UI)** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_shared_dialogs.py`<br/>`test_main_window.py` | Composants Qt (`ui/`) | Interaction offscreen sans serveur d'affichage, disposition des widgets, signaux/slots, sélection de listes, menus contextuels, zoom/pan, dialogues standardisés et boîtes modales (~97% de couverture). |
| **Contrôleurs** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | Contrôleurs (`src/controllers/`) | Coordination du pipeline en 5 phases (Persistance -> ETL -> Parquet -> Nettoyage), surbrillance visuelle, appariement des routes et synchronisation d'état. |
| **Noyau et DI** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder et Renderer | Injection complète des dépendances, rendu dans QGraphicsScene (rubans, nœuds, flèches directionnelles) et validation des schémas Pydantic. |
| **Agent SLM et Raisonnement** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | Pipeline SLM (`src/slm/`) | Inférence déterministe d'unités, désambiguïsation heuristique, extraction hiérarchique des clés, nettoyage de `<think>` et synthèse de prompts. |
| **Modèles de Domaine** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Émission réactive de signaux Qt (`map_data_loaded`, `data_sources_changed`), appariement de voies opposées et respect de l'invariant `_is_savable()`. |
| **Sous-Système ETL** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL et Transformateurs | Extraction multithread, hachage MD5, compression zlib, PRAGMAs SQLite WAL, aplatissement de payloads et compilation Polars. |
| **Couche de Services** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Services d'Arrière-Plan | Compilation AST Polars, conversion d'unités SI ($km/h$, $m/s$, $mph$), vitesse harmonique, export Parquet, parsing XML/GZ SUMO et `.sfm.json`. |
| **Utilitaires** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | Utilitaires et Matériel | Persistance de la configuration, résolution des traductions imbriquées, télémétrie CPU/VRAM, préchargement CUDA et repli CPU sécurisé. |

---

## 3. Stratégie d'Isolation et Mocking

1. **Plateforme Qt Headless Offscreen** : Les widgets sont instanciés sans écran actif via `QT_QPA_PLATFORM=offscreen`. `tests/conftest.py` configure une fixture `QApplication` partagée (`qapp`) et des mocks d'internationalisation (`mock_i18n`) et de configuration (`mock_config`).
2. **Mocks Déterministes d'IA** : Les tests de `SLMEngine` et `NeuroSymbolicResolver` utilisent des fixtures JSON déterministes sans nécessiter de GPU physique.
3. **Isolation SQLite WAL** : Le stockage temporaire utilise des bases de données SQLite éphémères avec mode WAL pour tester la concurrence multithread sans résidu.
4. **Sandboxing des Fichiers** : Toutes les écritures de fichiers de test (`.sfm.json`, bases SQLite, Parquet) sont exécutées dans la fixture `tmp_path` de pytest.
5. **Protection de Fermeture** : L'appel à `os._exit(0)` dans `MainWindow.closeEvent` est intercepté par `monkeypatch` pour éviter l'arrêt brutal du lanceur de tests.

---

## 🔗 Liens Utiles
* [Hub de Documentation](README.md)
* [Architecture](architecture.md)
* [Référence API](api_reference.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingénierie de Mobilité Intelligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Sous licence AGPLv3.</small>
</div>
