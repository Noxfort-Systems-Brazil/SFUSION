<div align="center">

<img src="../assets/sfusion-logo.png" alt="SFusion Mapper Logo" width="120" />

# SFusion Mapper — Suíte de Documentação Técnica
### Arquitetura de Sistemas, Descoberta Neural de Esquemas e Física Vetorial
*Noxfort Systems — A State Of Art Company*

[![Status](https://img.shields.io/badge/Status-Ativo-brightgreen?style=flat&logo=github)](https://github.com/Noxfort-Systems-Brazil/SFUSION)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![PySide6](https://img.shields.io/badge/Framework-PySide6%20(Qt6)-41CD52?style=flat&logo=qt&logoColor=white)](https://www.qt.io/)
[![Engine: Polars](https://img.shields.io/badge/Engine-Polars-CD792C?style=flat)](https://pola.rs/)
[![Format: Parquet](https://img.shields.io/badge/Output-Apache%20Parquet-teal?style=flat)](https://parquet.apache.org/)
[![Licença](https://img.shields.io/badge/Licenca-AGPL_v3-blue?style=flat)](../../LICENSE)

---

🌐 **Idiomas:** **[🇺🇸 English](../en/README.md)** • **[🇧🇷 Português (Brasil)](README.md)** • **[🇪🇸 Español](../es/README.md)** • **[🇫🇷 Français](../fr/README.md)** • **[🇷🇺 Русский](../ru/README.md)** • **[🇨🇳 简体中文](../zh/README.md)** • **[📖 Central de Documentação](../README.md)**

---

</div>

## Bem-vindo à Documentação Técnica Oficial

Este diretório reúne toda a suíte de documentação técnica em **Português do Brasil** do **SFusion Mapper** (SYNAPSE Fusion) — a ferramenta visual de engenharia de dados "Day Zero" e normalização cinemática desenvolvida pela Noxfort Systems. O SFusion conecta fluxos heterogêneos de telemetria urbana (Waze, TomTom, laços indutivos, radares) com ambientes estritos de simulação microscópica de tráfego (como o SUMO).

## Índice de Guias Especializados

| Documento | Tema & Escopo | Principais Tópicos |
| :--- | :--- | :--- |
| 📚 **[Central Master de Documentação (MOC)](sfusion_moc.md)** | Índice e Vault Obsidian | Mapa mestre de navegação, estrutura detalhada de diretórios e grafo de conhecimento. |
| 🏛️ **[Arquitetura do Sistema](architecture.md)** | Especificação de Arquitetura | Clean MVC, injeção de dependência via padrão Builder, camada View em PySide6, serviços em background e AppState reativo como Fonte Única da Verdade. |
| 📖 **[Conceitos Fundamentais](core_concepts.md)** | Fundamentos Teóricos | Paradigma "Day Zero", topologia em grafo do SUMO (MapNode/MapEdge), inferência neuro-simbólica e arquitetura Medalhão (Bronze/Prata/Ouro). |
| 🗃️ **[Modelos de Dados e Esquemas](data_models.md)** | Dicionário de Dados | Entidades de domínio imutáveis, contrato Pydantic v2 `KinematicMap`, tabelas de staging SQLite WAL e esquema final unificado Apache Parquet. |
| ⚡ **[Pipeline ETL de Alta Performance](etl_pipeline.md)** | Motor de Ingestão | Orquestração multithread com `QThreadPool`, `SensorBatchProcessor`, hashing MD5, compressão zlib e afinação PRAGMA de concorrência em SQLite WAL. |
| 📐 **[Motor Físico Vetorial](math_engine.md)** | Compilação Polars AST | Transformações vetoriais SIMD sem travas de GIL, normalização de unidades SI ($km/h$, $m/s$, $mph$), Velocidade Média Espacial Harmônica e densidade $k = q / v$. |
| 🧠 **[Pipeline Neural (SLM)](neural_pipeline.md)** | Raciocínio de IA Local | Modelo quantizado *Phi-4-mini* GGUF integrado, runtime `llama.cpp`, extração hierárquica de chaves, filtragem de tokens `<think>` e `NeuroSymbolicResolver`. |
| 🚀 **[Aceleração por Hardware e CUDA](hardware_and_cuda.md)** | Infraestrutura de GPU | Carregador dinâmico de bibliotecas CUDA (`ensure_cuda_libs`), `slm_settings.json`, uso de TensorCores, fallback para CPU e telemetria do sistema. |
| 🔄 **[Fluxo de Trabalho do Sistema](system_workflow.md)** | Ciclo de Vida dos Dados | Execução determinística em 5 fases: Ingestão de Topologia, Registro de Sensores, Associação e Descoberta, Staging ETL e Exportação Parquet. |
| 🖥️ **[Manual de Operações e Guia do Usuário](user_guide.md)** | Manual do Operador | Navegação interativa na tela (pan/zoom), pareamento bidirecional de vias, associação local e global, override manual e projetos `.sfm.json`. |
| 🛠️ **[Guias de Desenvolvimento e Extensão](developer_guides.md)** | Manual do Desenvolvedor | Configuração do ambiente, injeção com `AppBuilder`, novos extratores de sensores, regras de concorrência e testes. |
| 📦 **[Implantação, Empacotamento e Containers](deployment_and_packaging.md)** | Engenharia de Release | Compilação com PyInstaller via `sfusion.spec`, Docker multi-stage e integração desktop no Linux. |
| 🧪 **[Diretrizes de Testes e Qualidade](testing.md)** | Padrões de QA | 160 testes automatizados com Pytest, cobertura >91% no backend e frontend, execução headless Qt, mocks de IA e divisão em 10 módulos. |
| ⚡ **[Referência da API Interna](api_reference.md)** | Contratos de Classes e Sinais | Especificação técnica do estado de domínio, serviços, padrões DAO/Repository, sinais Qt e mediação dos controladores. |

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Engenharia de Mobilidade Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
