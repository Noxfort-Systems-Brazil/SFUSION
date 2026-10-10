---
tags: [desenvolvimento, guia, setup, mvc, builder, polars, slm, testes]
aliases: [Guias de Desenvolvimento, Referência do Desenvolvedor, Guia de Contribuição]
---

# 🛠️ Guias de Desenvolvimento e Extensão

Este documento fornece instruções passo a passo para configuração do ambiente de desenvolvimento, compreensão dos padrões Clean MVC e Builder, extensão de novos extratores de sensores, compilação de fórmulas físicas no Polars e execução da suíte de testes automatizados.

⬅️ [Central Master de Documentação](sfusion_moc.md) | 🏛️ [Arquitetura do Sistema](architecture.md) | ⚡ [Pipeline ETL](etl_pipeline.md) | 🧪 [Diretrizes de Testes](testing.md)

---

## 1. Configuração do Ambiente de Desenvolvimento

### 1.1 Pré-requisitos de Sistema
O SFusion Mapper requer **Python 3.9+** (recomendado 3.10–3.12) e **PySide6 (Qt6)**. Em distribuições Linux Ubuntu/Debian, instale os pacotes gráficos e de compilação essenciais:

```bash
sudo apt update
sudo apt install -y \
    python3-venv \
    build-essential \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6dbus6 \
    libxkbcommon-x11-0 \
    libgl1 \
    libxcb-cursor0
```

### 1.2 Ambiente Virtual e Dependências
Clone o repositório e inicialize o ambiente virtual:

```bash
git clone https://github.com/Noxfort-Systems-Brazil/SFUSION.git
cd SFUSION

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 1.3 Modelo SLM Quantizado
O mecanismo de inferência neuro-simbólica utiliza o modelo **Phi-4-mini-reasoning GGUF** localizado no diretório `src/models/`:

```bash
src/models/Phi-4-mini-reasoning-UD-Q6_K_XL.gguf
```

Caso o modelo não esteja presente ou a máquina não disponha de GPU, o sistema ativa automaticamente o fallback para heurísticas determinísticas através do `NeuroSymbolicResolver`.

---

## 2. Padrões de Arquitetura e Clean MVC

O SFusion isola estritamente as responsabilidades entre as camadas:

```text
View (ui/) <---> Controller (src/controllers/) <---> Model (src/domain/ & AppState)
                          │
                          ▼
              Serviços (src/services/ & src/etl/)
                          │
                          ▼
              Subsistema SLM (src/slm/)
```

### 2.1 Injeção de Dependências com `AppBuilder`
Nenhuma visualização ou controlador deve instanciar dependências diretamente. A inicialização completa é coordenada por [`src/core/app_builder.py`](../../src/core/app_builder.py):

```python
builder = AppBuilder()
builder.create_domain()
builder.create_services()
builder.create_controllers()
builder.create_views()
builder.wire_signals()
app_window = builder.build()
```

### 2.2 Concorrência e Segurança de Threads
- **Thread Principal da GUI:** Nunca execute I/O de disco, consultas pesadas, compilações Polars AST ou inferência de LLM na thread do PySide6.
- **Workers em Segundo Plano:** Tarefas assíncronas devem ser despachadas via `QThreadPool` ou subclasses de `QThread` (como `SensorBatchProcessor` e `ParquetExportWorker`).
- **Comunicação por Sinais:** Os controladores recebem notificações e dados dos workers exclusivamente através de Qt Signals.

---

## 3. Extensão de Extratores de Sensores (`src/services/extractors.py`)

Para adicionar suporte a um novo formato de arquivo ou protocolo de sensor:

1. Crie uma classe herdando de `BaseExtractor`.
2. Implemente a extração de cabeçalhos e amostragem leve:

```python
from src.services.extractors import BaseExtractor

class MeuExtratorSensor(BaseExtractor):
    def extract_headers(self, file_path: str) -> list[str]:
        # Leitura e retorno das chaves do arquivo
        ...
        
    def sample_records(self, file_path: str, limit: int = 10) -> list[dict]:
        # Retorna amostra leve para a prévia da SLM
        ...
```

3. Registre o extrator no método `register_extractor()` em [`src/services/data_importer.py`](../../src/services/data_importer.py).

---

## 4. Compilação de Física Vetorial (`src/services/math_engine.py`)

As fórmulas de conversão e normalização física são expressas como expressões Polars (`pl.Expr`) compiladas e executadas sem contenção do GIL de Python:

```python
import polars as pl

# Exemplo: Conversão de km/h para metros por segundo (m/s)
velocidade_mps = pl.col("velocidade_kmh") * (1000.0 / 3600.0)

# Cálculo da Velocidade Média Harmônica Espacial
velocidade_harmonica = pl.count() / (1.0 / pl.col("velocidade_mps")).sum()
```

---

## 5. Diretrizes de Testes Automatizados

Mantemos o padrão de cobertura mínima de **80%** (suíte atual com **169 testes e >91% de cobertura global**).

### 5.1 Execução Headless
Todos os testes rodam em modo offscreen sem abrir janelas gráficas:

```bash
# Executa toda a suíte de testes
QT_QPA_PLATFORM=offscreen pytest

# Executa com relatório de tempos e verbosidade
QT_QPA_PLATFORM=offscreen pytest -v --durations=10

# Gera relatório de cobertura no terminal
QT_QPA_PLATFORM=offscreen pytest --cov=src --cov=ui --cov-report=term-missing
```

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Engenharia de Mobilidade Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
