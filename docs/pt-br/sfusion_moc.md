---
tags: [moc, hub, docs, obsidian, sfusion, indice]
aliases: [SFUSION MOC, Central Master de Documentação, Índice de Documentação, Vault de Conhecimento]
---

# 📚 SFusion: Central Master de Documentação Técnica (MOC)

Bem-vindo à biblioteca técnica do **SFusion Mapper** (SYNAPSE Fusion). Projetado como um aplicativo de engenharia de dados e interface gráfica de alta performance para ecossistemas de mobilidade inteligente, o SFusion integra redes microscópicas do SUMO, fluxos de sensores heterogêneos, inferência neuro-simbólica local via SLM e compilação vetorial com Polars.

Este índice mestre de documentação fornece cobertura técnica profunda para desenvolvedores de núcleo, engenheiros de simulação, cientistas de dados de tráfego e integradores de sistemas. É 100% compatível tanto com o **GitHub** quanto com o **[Obsidian](https://obsidian.md/)**.

⬅️ [Central em Português](README.md) | 🏛️ [Arquitetura do Sistema](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md) | 📐 [Motor Físico Polars](math_engine.md)

---

## 🗺️ Mapa da Base de Código e Hierarquia de Diretórios

```text
SFUSION/
├── sfusion.py                  # Ponto de Entrada Mestre (AppBuilder, SingleInstance, Ciclo GUI)
├── ARCHITECTURE.md             # Blueprint Clean MVC, Padrão Builder & Camada de Serviços
├── pyproject.toml              # Toolchain de build e metadados do projeto
├── requirements.txt            # Dependências de execução em Python
├── sfusion.spec                # Especificação de empacotamento standalone do PyInstaller
├── Dockerfile                  # Container multi-stage de build Linux
├── docker-compose.yml          # Definição de composição Docker
├── sync.sh                     # Script de sincronização e push 1-clique com GitHub
├── run.sh                      # Script de inicialização com ambiente virtual
│
├── config/                     # Sistemas de Configuração
│   └── default_settings.json   # Hiperparâmetros base da aplicação
│
├── locale/                     # Traduções da Interface Gráfica (PySide6)
│   ├── en_us.json              # Inglês (EUA)
│   ├── pt_br.json              # Português do Brasil
│   ├── es_es.json              # Espanhol
│   ├── fr_fr.json              # Francês
│   ├── ru_ru.json              # Russo
│   └── zh_cn.json              # Chinês Simplificado
│
├── locale_backend/             # Traduções de Workers em Background e Telemetria
│   ├── en_us.json              # Inglês (EUA)
│   ├── pt_br.json              # Português do Brasil
│   ├── es_es.json              # Espanhol
│   ├── fr_fr.json              # Francês
│   ├── ru_ru.json              # Russo
│   └── zh_cn.json              # Chinês Simplificado
│
├── docs/                       # Vault Geral de Documentação Técnica
│   ├── SFUSION_MOC.md          # Master Documentation Hub (Em Inglês)
│   ├── pt-br/                  # Suíte Completa em Português do Brasil
│   │   ├── sfusion_moc.md      # Central Master MOC (Este Arquivo)
│   │   ├── README.md           # Hub Central em Português
│   │   ├── architecture.md     # Arquitetura Técnica & Padrões
│   │   ├── core_concepts.md    # Paradigma Day Zero & Grafos SUMO
│   │   ├── data_models.md      # Entidades de Domínio, KinematicMap & Parquet
│   │   ├── etl_pipeline.md     # Motor de Ingestão & Staging SQLite WAL
│   │   ├── math_engine.md      # Motor Físico Vetorial & Polars AST
│   │   ├── neural_pipeline.md  # SLM Phi-4-mini & Resolvedor Neuro-Simbólico
│   │   ├── hardware_and_cuda.md # Aceleração GPU NVIDIA & Dynamic CUDA Loader
│   │   ├── system_workflow.md  # Ciclo de Vida dos Dados em 5 Fases
│   │   ├── user_guide.md       # Manual de Operações da Interface Gráfica
│   │   ├── developer_guides.md # Guias de Desenvolvimento & Extensibilidade
│   │   ├── deployment_and_packaging.md # Empacotamento PyInstaller & Docker
│   │   ├── testing.md          # Diretrizes de Testes (>91% de Cobertura)
│   │   └── api_reference.md    # Referência Técnica de APIs & Sinais Qt
│   └── ...
│
├── src/                        # Código-fonte Principal em Python
│   ├── agent/                  # Orquestração de alto nível (Fachada SLMEngine)
│   ├── controllers/            # Controladores de Subsistemas (Map, Sources, Info, Settings)
│   ├── core/                   # Injeção de Dependências (AppBuilder), Schemas, MapRenderer
│   ├── domain/                 # Modelo de Domínio (AppState SSOT, Entidades imutáveis)
│   ├── etl/                    # SensorBatchProcessor & SQLite WAL StorageRepository
│   ├── models/                 # Modelos neurais quantizados GGUF (Phi-4-mini)
│   ├── services/               # Importadores, ParquetService, MathEngine Polars, Persistência
│   ├── slm/                    # Camada SLM de baixo nível (llama.cpp, PromptBuilder, Parser)
│   └── utils/                  # CUDALoader, I18nManager, SLMTelemetry, Config
│
├── ui/                         # Componentes Desktop da Interface PySide6
│   ├── editor/                 # Painel editor de mapeamento sensor-topologia
│   ├── map/                    # Canvas vetorial interativo QGraphicsView
│   ├── settings/               # Diálogos de configuração e offload de hardware
│   ├── shared/                 # Widgets e caixas de diálogo compartilhadas
│   ├── sources/                # Inspetor de diretório de sensores e árvore de arquivos
│   └── main_window.py          # Janela principal e orquestrador de layout
│
└── tests/                      # Suíte de Testes Automatizados (160 testes, >91% cobertura)
    ├── test_controllers/       # Testes de mediação de controladores e sinais
    ├── test_core/              # Testes do AppBuilder, esquemas e MapRenderer
    ├── test_domain/            # Testes de transição de estado e entidades
    ├── test_etl/               # Testes de processamento em lote e SQLite WAL
    ├── test_services/          # Testes de importação, física Polars e exportação Parquet
    ├── test_slm/               # Testes de prompt, filtro <think> e resolução heurística
    ├── test_ui/                # Testes headless de interface gráfica Qt
    └── test_utils/             # Testes de carregamento CUDA e internacionalização
```

---

## 📖 Dimensões do Sistema e Navegação no Conhecimento

### 1. Infraestrutura Central e Engenharia de Dados
- **[Arquitetura do Sistema](architecture.md)**: Blueprint técnico detalhando Clean MVC, padrão Builder com injeção de dependência e threads desacopladas.
- **[Pipeline ETL de Alta Performance](etl_pipeline.md)**: Especificações da ingestão paralela de sensores, `SensorBatchProcessor`, hashing MD5 de lotes e persistência em SQLite WAL.
- **[Modelos de Dados e Esquemas](data_models.md)**: Entidades imutáveis de domínio, contrato Pydantic v2 `KinematicMap` e esquema unificado Apache Parquet.
- **[Motor Físico Vetorial](math_engine.md)**: Compilador Polars AST (`pl.Expr`), operações vetoriais SIMD, normalização para o SI e Velocidade Média Harmônica.

### 2. Inteligência Artificial e Inferência Neuro-Simbólica
- **[Pipeline Neural (SLM)](neural_pipeline.md)**: Modelo de Linguagem Pequeno (Phi-4-mini GGUF via `llama.cpp`), offload de camadas GPU e dimensionamento de contexto.
- **[Resolvedor Neuro-Simbólico](neural_pipeline.md#resolucao-neuro-simbolica)**: Validação heurística e física isolando tokens de raciocínio `<think>` e assegurando limites determinísticos.
- **[Ciclo de Vida do Sistema](system_workflow.md)**: Execução determinística em 5 fases (Ingestão de Topologia, Registro de Sensores, Mapeamento, Staging ETL e Exportação Parquet Ouro).

### 3. Aceleração de Hardware e Gráficos
- **[Aceleração por Hardware e CUDA](hardware_and_cuda.md)**: Carregamento dinâmico de bibliotecas NVIDIA (`libcudart.so`, `libcublas.so`), offload de VRAM e fallback transparente para CPU.
- **[Conceitos Fundamentais](core_concepts.md)**: Fundamentos teóricos do paradigma Day Zero, topologias SUMO e integração com ecossistemas a jusante (CARINA e SYNAPSE).

### 4. Operações, Interface Desktop e Garantia de Qualidade
- **[Manual de Operações e Guia do Usuário](user_guide.md)**: Tutorial visual passo a passo para navegação, pareamento de vias, associação de colunas e geração do dataset.
- **[Guias de Desenvolvimento e Extensão](developer_guides.md)**: Configuração do ambiente de desenvolvimento, padrões de codificação, criação de novos parsers e testes.
- **[Implantação, Empacotamento e Containers](deployment_and_packaging.md)**: Compilação de binários nativos com PyInstaller via `sfusion.spec`, containers Docker multi-stage e integração desktop Linux.
- **[Diretrizes de Testes e Qualidade](testing.md)**: Suíte com 160 testes cobrindo >91% do código, execução headless no PySide6 e mocks determinísticos.
- **[Referência da API Interna](api_reference.md)**: Especificações de contratos de classes, sinais Qt, repositórios e controladores.

---

> 💡 **Grafo de Conhecimento Obsidian:** Esta documentação possui suporte nativo integral ao [Obsidian](https://obsidian.md/). Abra a pasta raiz do `SFUSION` como um Vault do Obsidian para navegar pelo grafo interativo e backlinks.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Engenharia de Mobilidade Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
