# 🧪 Directrices de Pruebas y Validación de Calidad

SFusion cuenta con **160 pruebas automáticas** en Pytest que cubren >91% de los subsistemas de dominio, interfaz visual (UI), controladores, ETL, modelos físicos y análisis SLM.

⬅️ [Centro de Documentación](README.md) | 🏛️ [Arquitectura](architecture.md) | ⚡ [Referencia de API](api_reference.md)

---

## 1. Ejecución de Pruebas

### 1.1 Ejecutar Todas las Pruebas Automatizadas
Utilizando el entorno virtual con PySide6 en modo headless (offscreen):
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 Generación de Reporte de Cobertura de Código
Para medir cobertura de líneas y bifurcaciones en el backend (`src/`) y frontend (`ui/`):
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
El reporte HTML interactivo se generará en `htmlcov/index.html`. SFusion mantiene **>91% de cobertura global** (Frontend: **~97%**, Backend: **~89%**).

---

## 2. Resumen de Módulos (160 Pruebas en 10 Módulos)

| Módulo de Prueba | Archivo de Prueba | Componente Evaluado | Comportamientos Verificados |
| :--- | :--- | :--- | :--- |
| **Vistas de Frontend** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_main_window.py` | Componentes Qt (`ui/`) | Interacción offscreen sin servidor gráfico, layouts, señales/slots, selección en listas, menús contextuales, pan/zoom y diálogos modales (~97% cobertura). |
| **Controladores** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | Controladores (`src/controllers/`) | Coordinación del pipeline en 5 fases (Persistencia -> ETL -> Parquet -> Limpieza), resaltado visual, emparejamiento de vías y sincronización. |
| **Núcleo y DI** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder y Renderizador | Inyección de dependencias completa, dibujo en QGraphicsScene (cintas, nodos, flechas direccionales) y validación Pydantic. |
| **Agente SLM y Razonamiento** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | Pipeline SLM (`src/slm/`) | Inferencia determinista de unidades, resolución heurística de esquemas, extracción jerárquica de claves, filtrado de `<think>` y síntesis de prompts. |
| **Modelos de Dominio** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Despacho reactivo de señales Qt (`map_data_loaded`, `data_sources_changed`), emparejamiento direccional de vías y validación del invariante `_is_savable()`. |
| **Subsistema ETL** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL y Transformadores | Extracción multihilo, hash MD5, compresión zlib, directivas PRAGMA de SQLite WAL, aplanamiento de cargas y compilación física en Polars. |
| **Capa de Servicios** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Servicios de Fondo | Compilación Polars AST, conversiones de unidades SI ($km/h$, $m/s$, $mph$), velocidad armónica media, exportación Parquet, parsing SUMO XML/GZ y serialización `.sfm.json`. |
| **Utilidades** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | Utilidades y Hardware | Persistencia de configuraciones, resolución de traducciones anidadas, telemetría CPU/VRAM, detección dinámica de objetos compartidos CUDA y fallback seguro. |

---

## 3. Estrategia de Aislamiento y Mocks

1. **Plataforma Qt Headless Offscreen**: Los widgets se instancian sin pantalla activa mediante `QT_QPA_PLATFORM=offscreen`. `tests/conftest.py` define la fixture `qapp` e inyecta mocks para traducción (`mock_i18n`) y configuración (`mock_config`).
2. **Mocks Deterministas de IA**: Las pruebas de `SLMEngine` y `NeuroSymbolicResolver` usan respuestas JSON estáticas, garantizando ejecución veloz sin GPU física.
3. **Aislamiento SQLite WAL**: El almacenamiento ETL utiliza bases de datos SQLite temporales con modo WAL para probar transacciones multihilo seguras.
4. **Sandboxing de Archivos**: Los archivos generados (`.sfm.json`, SQLite staging y Parquet) se alojan en la fixture `tmp_path` de pytest con verificación de eliminación.
5. **Protección de Salida**: `MainWindow.closeEvent` llama a `os._exit(0)`, lo cual es interceptado con `monkeypatch` en los tests para evitar cerrar pytest prematuramente.

---

## 🔗 Enlaces Relacionados
* [Centro de Documentación](README.md)
* [Arquitectura](architecture.md)
* [Referencia de API](api_reference.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Ingeniería de Movilidad Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado bajo AGPLv3.</small>
</div>
