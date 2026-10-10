# 🧪 Diretrizes de Testes e Validação de Qualidade

O SFusion é responsável pela transformação exata de dados que alimentam simuladores urbanos e modelos de IA. Confiabilidade absoluta de dados, segurança em operações multithread com SQLite e precisão nas conversões cinemáticas exigem testes automatizados rigorosos.

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | ⚡ [Referência de API](api_reference.md)

---

## 1. Execução da Suíte de Testes

### 1.1 Executar Todos os Testes Automatizados
Utilizando o ambiente virtual local com PySide6 em modo headless:
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v
```

### 1.2 Gerar Relatório de Cobertura de Código
Para medir a cobertura de linhas e ramos tanto no backend (`src/`) quanto no frontend (`ui/`):
```bash
QT_QPA_PLATFORM=offscreen ./.venv/bin/pytest tests/ -v --cov=src --cov=ui --cov-report=term-missing --cov-report=html
```
O relatório HTML interativo será gerado em `htmlcov/index.html`. O SFusion alcança **>91% de cobertura total** (Frontend: **~97%**, Backend: **~89%**).

---

## 2. Estrutura da Suíte (169 Testes em 10 Módulos)

A suíte em `tests/` reúne **169 testes automatizados** cobrindo regras de negócio, interface gráfica, controladores, contratos Pydantic, concorrência no ETL e inferência do SLM:

| Módulo de Teste | Arquivo de Teste | Alvo Testado | Comportamentos Verificados |
| :--- | :--- | :--- | :--- |
| **Interface Visual (UI)** | `test_editor_panel.py`<br/>`test_sources_panel.py`<br/>`test_map_view.py`<br/>`test_settings_dialog.py`<br/>`test_shared_dialogs.py`<br/>`test_main_window.py` | Componentes Qt (`ui/`) | Interação offscreen sem servidor X11/Wayland, layouts de widgets, sinais/slots, seleção em lista, menus de contexto, pan/zoom, diálogos padronizados e diálogo modal (~97% de cobertura). |
| **Controladores** | `test_main_controller.py`<br/>`test_info_controller.py`<br/>`test_map_controller.py`<br/>`test_sources_controller.py`<br/>`test_settings_controller.py` | Controladores (`src/controllers/`) | Coordenação das 5 fases do pipeline (Persistência -> ETL -> Parquet -> Limpeza), destaque visual, pareamento de vias e sincronização com AppState. |
| **Core e DI** | `test_app_builder.py`<br/>`test_map_renderer.py`<br/>`test_schemas.py` | App Builder e Renderizador | Injeção de dependências completa, renderização gráfica (ribbon stroker, junções, setas direcionais) e validação Pydantic. |
| **Agente SLM e Raciocínio** | `test_slm_engine.py`<br/>`test_neuro_symbolic_resolver.py`<br/>`test_prompt_builder.py`<br/>`test_slm_output_parser.py` | Pipeline SLM (`src/slm/`) | Inferência determinística de unidades, resolução heurística de esquemas, extração hierárquica de chaves, filtragem de `<think>` e geração de prompts. |
| **Modelos de Domínio** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Emissão reativa de sinais Qt (`map_data_loaded`, `data_sources_changed`), pareamento bidirecional de vias, associações e invariante `_is_savable()`. |
| **Subsistema ETL** | `test_sensor_processor.py`<br/>`test_storage_repository.py`<br/>`test_etl_service.py`<br/>`test_neural_transformer.py` | ETL e Transformadores | Extração multithread, hash MD5, compressão zlib, PRAGMAs do SQLite WAL, descompactação de payloads e compilação física no Polars. |
| **Camada de Serviços** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Serviços em Background | Compilação Polars AST, conversões SI ($km/h$, $m/s$, $mph$), média harmônica, exportação Parquet, parsing SUMO XML/GZ e serialização `.sfm.json`. |
| **Utilitários** | `test_cuda_loader.py`<br/>`test_config.py`<br/>`test_i18n.py`<br/>`test_slm_telemetry.py` | Utils e Hardware | Persistência de configurações, resolução de traduções aninhadas, telemetria de CPU/VRAM, carregamento de SOs da CUDA e fallback seguro. |

---

## 3. Estratégia de Isolamento e Mocking

1. **Plataforma Qt Headless Offscreen**: Os widgets do PySide6 são instanciados e validados em modo headless através de `QT_QPA_PLATFORM=offscreen`. O arquivo `tests/conftest.py` define uma fixture compartilhada de `QApplication` (`qapp`) e mocks para internacionalização (`mock_i18n`) e configurações (`mock_config`), viabilizando a execução em ambientes de CI sem servidor gráfico.
2. **Mocks Determinísticos para SLM**: Os testes de `SLMEngine`, `LLMInferenceProvider` e `NeuroSymbolicResolver` utilizam respostas JSON fixas e mocks com `unittest.mock`, garantindo validação ultrarrápida sem depender de hardware GPU dedicado ou dos 3.5GB de pesos do modelo.
3. **Isolamento de Staging no SQLite**: Os testes de banco utilizam arquivos temporários com modo WAL ativado, validando escrita e concorrência multithread sem persistir lixo no repositório.
4. **Sandboxing de Arquivos Temporários**: Todos os testes que geram arquivos (projetos `.sfm.json`, bases SQLite temporárias e datasets Parquet) operam na fixture `tmp_path` do pytest e verificam a autolimpeza pós-processamento.
5. **Proteção Contra Encerramento de Processo**: O método `MainWindow.closeEvent` executa `os._exit(0)` em produção; os testes interceptam essa chamada via `monkeypatch.setattr(os, "_exit", mock_exit)` para permitir o encerramento gracioso sem abortar o executor do pytest.

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Arquitetura Técnica](architecture.md)
* [Referência de API](api_reference.md)

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Engenharia de Mobilidade Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
