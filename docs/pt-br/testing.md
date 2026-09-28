# 🧪 Diretrizes de Testes e Validação de Qualidade

O SFusion é responsável pela transformação exata de dados que alimentam simuladores urbanos e modelos de IA. Confiabilidade absoluta de dados, segurança em operações multithread com SQLite e precisão nas conversões cinemáticas exigem testes automatizados rigorosos.

⬅️ [Central de Documentação](README.md) | 🏛️ [Arquitetura](architecture.md) | ⚡ [Referência de API](api_reference.md)

---

## 1. Execução da Suíte de Testes

### 1.1 Executar Todos os Testes Automatizados
```bash
./.venv/bin/pytest tests/ -v
```

### 1.2 Gerar Relatório de Cobertura de Código
```bash
./.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

---

## 2. Estrutura da Suíte (66 Testes em 8 Módulos)

| Módulo de Teste | Arquivo de Teste | Alvo Testado | Comportamentos Verificados |
| :--- | :--- | :--- | :--- |
| **Agente SLM** | `test_slm_engine.py` | Fachada `SLMEngine` | Orquestração da descoberta de esquema, formatação de prompt, inferência simulada e fallback. |
| **Controladores** | `test_main_controller.py` | `MainController` | Coordenação do ciclo de vida, salvar/abrir projetos, criação da base de staging (`.temp_sfusion_*.db`) e limpeza. |
| **Esquemas Centrais** | `test_schemas.py` | `KinematicMap` (Pydantic) | Validação tipada, restrições padrão, enumeração de unidades e serialização. |
| **Modelos de Domínio** | `test_app_state.py`<br/>`test_entities.py` | `AppState`<br/>`DataSource`, `MapEdge`, `MapNode` | Emissão reativa de sinais Qt (`map_data_loaded`, `data_sources_changed`), pareamento viário e invariante `_is_savable()`. |
| **Subsistema ETL** | `test_sensor_processor.py`<br/>`test_storage_repository.py` | `SensorBatchProcessor`<br/>`ETLStorageRepository` | Extração multithread, hash MD5, compressão zlib, PRAGMAs do SQLite WAL e transações seguras. |
| **Camada de Serviços** | `test_math_engine.py`<br/>`test_parquet_service.py`<br/>`test_data_importer.py`<br/>`test_map_importer.py`<br/>`test_persistence.py`<br/>`test_project_service.py`<br/>`test_extractors.py` | Serviços em Background | Compilação Polars AST, conversões SI ($km/h$, $m/s$, $mph$), média harmônica, exportação Parquet, parsing SUMO e `.sfm.json`. |
| **Parsing SLM** | `test_slm_output_parser.py` | `SLMOutputParser` | Extração de JSON puro da resposta do modelo, eliminando tags `<think>...</think>`, markdown fences e preâmbulos. |
| **Utilitários** | `test_cuda_loader.py` | `cuda_loader.py` | Localização dinâmica de bibliotecas CUDA empacotadas via pip (`libcudart.so`, `libcublas.so`), pré-carga e fallback CPU. |

---

## 🔗 Documentos Relacionados
* [Central de Documentação](README.md)
* [Arquitetura Técnica](architecture.md)
* [Referência de API](api_reference.md)
