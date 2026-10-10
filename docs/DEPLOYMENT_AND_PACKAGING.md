---
tags: [deployment, packaging, docker, pyinstaller, desktop]
aliases: [Deployment Guide, Packaging, Docker, Standalone Binary]
---

# 🚀 Deployment, Packaging & Containerization

This document details production deployment and packaging options for **SFusion Mapper**, including Docker containerization, standalone PyInstaller binary builds, and Linux desktop integration.

⬅️ Back to [Main Documentation Hub](SFUSION_MOC.md) | 🛠️ See [Developer Guides](DEVELOPER_GUIDES.md) | 🏛️ See [Architecture](ARCHITECTURE.md) | 🧪 See [Testing](TESTING.md)

---

## 1. Production Docker Containerization (`Dockerfile`)

SFusion includes an optimized Docker build configuration based on `python:3.12-slim-bookworm` equipped with required Qt6, X11, and font libraries to run the application directly inside containerized or headless environments.

### 1.1 Building the Container Image
```bash
docker build -t sfusion-mapper:latest .
```

### 1.2 Running Headless Testing via Docker Compose
Using the included [`docker-compose.yml`](../docker-compose.yml):

```bash
docker compose up --build
```

---

## 2. Standalone Binary Compilation with PyInstaller

For municipal and desktop deployment without requiring Python runtime installation on client machines, SFusion can be bundled into a standalone executable:

### 2.1 Installing Packaging Toolchain
```bash
pip install pyinstaller
```

### 2.2 Generating Standalone Executable
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

The compiled standalone executable will be located in `dist/sfusion-mapper/`.

---

## 3. Linux Desktop Integration (`.desktop`)

To integrate SFusion Mapper into Linux desktop application menus (GNOME, KDE Plasma, XFCE):

Create `~/.local/share/applications/sfusion.desktop`:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=SFusion Mapper
GenericName=Traffic ETL & Kinematic Normalization Tool
Comment=Day Zero configuration and transformation engine for smart mobility
Exec=/opt/sfusion/run.sh
Icon=/opt/sfusion/docs/assets/sfusion-logo.png
Terminal=false
Categories=Science;Engineering;Development;
Keywords=SUMO;Traffic;Simulation;ETL;Polars;Parquet;
```

Update desktop application database:
```bash
update-desktop-database ~/.local/share/applications/
```

---

## 4. Hardware & NVIDIA Runtime Configuration

When deploying on workstations with NVIDIA GPUs:
1. Ensure NVIDIA Driver $\ge 525.60$ is installed.
2. Install the CUDA Toolkit 12.x or verify that pip packages provide runtime libraries (`nvidia-cuda-runtime-cu12`, `nvidia-cublas-cu12`).
3. SFusion automatically runs [`src/utils/cuda_loader.py`](../src/utils/cuda_loader.py) on startup to link `libcudart.so` and `libcublas.so` dynamically into the runtime environment.

---

<div align="center">
  <img src="assets/noxfort-logo.png" alt="Noxfort Systems Logo" width="45" /><br/>
  <b>Noxfort Systems</b> — <i>A State Of Art Company</i><br/>
  <i>SYNAPSE Fusion (SFusion) Mapper • Version 0.1.0</i><br/>
  <small>© 2026 Noxfort Systems. Licenciado sob AGPLv3.</small>
</div>
