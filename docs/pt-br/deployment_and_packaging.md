---
tags: [implantacao, empacotamento, docker, pyinstaller, desktop]
aliases: [Guia de Implantação, Empacotamento, Docker, Binário Nativo]
---

# 🚀 Implantação, Empacotamento e Containers

Este documento detalha os procedimentos de empacotamento para ambientes de produção e homologação do **SFusion Mapper**, incluindo containerização com Docker, compilação de binários nativos com PyInstaller e integração com ambientes desktop Linux.

⬅️ [Central Master de Documentação](sfusion_moc.md) | 🛠️ [Guias de Desenvolvimento](developer_guides.md) | 🏛️ [Arquitetura](architecture.md) | 🧪 [Testes](testing.md)

---

## 1. Containerização com Docker (`Dockerfile`)

O SFusion possui um [`Dockerfile`](../../Dockerfile) otimizado baseado na imagem `python:3.12-slim-bookworm`, projetado para compilação e execução de testes em esteiras de integração contínua (CI/CD).

### 1.1 Construção da Imagem Docker
```bash
docker build -t sfusion-mapper:latest .
```

### 1.2 Execução com Docker Compose
Através do arquivo [`docker-compose.yml`](../../docker-compose.yml):

```bash
docker compose up --build
```

---

## 2. Compilação de Executável Standalone com PyInstaller

Para implantação em estações municipais ou computadores de operadores que não possuam interpretador Python instalado:

### 2.1 Instalação do PyInstaller
```bash
pip install pyinstaller
```

### 2.2 Geração do Binário Standalone
```bash
pyinstaller \
  --name "sfusion-mapper" \
  --windowed \
  --icon "docs/assets/sfusion-logo.png" \
  --add-data "locale:locale" \
  --add-data "locale_backend:locale_backend" \
  --add-data "config:config" \
  --add-data "docs/assets:docs/assets" \
  sfusion.py
```

O binário final compilado será gerado no diretório `dist/sfusion-mapper/`.

---

## 3. Integração Desktop no Linux (`.desktop`)

Para que o SFusion Mapper apareça no menu de aplicativos do sistema operacional (GNOME, KDE Plasma, XFCE):

Crie o arquivo `~/.local/share/applications/sfusion.desktop`:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=SFusion Mapper
GenericName=Ferramenta de Configuração ETL e Normalização Cinemática
Comment=Motor de ingestão Day Zero para ecossistemas de mobilidade inteligente
Exec=/opt/sfusion/run.sh
Icon=/opt/sfusion/docs/assets/sfusion-logo.png
Terminal=false
Categories=Science;Engineering;Development;
Keywords=SUMO;Transito;Simulacao;ETL;Polars;Parquet;
```

Atualize o banco de dados de aplicativos:
```bash
update-desktop-database ~/.local/share/applications/
```

---

## 4. Configuração de Hardware e Driver NVIDIA

Ao executar em computadores com placas de vídeo dedicadas NVIDIA:
1. Certifique-se de que o driver NVIDIA ($\ge 525.60$) esteja instalado.
2. O script [`src/utils/cuda_loader.py`](../../src/utils/cuda_loader.py) é executado automaticamente na inicialização, detectando e pré-carregando os binários `libcudart.so` e `libcublas.so` em tempo de execução.

---

<div align="center">
  <img src="../assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>Engenharia de Mobilidade Inteligente • SFusion Mapper v0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
