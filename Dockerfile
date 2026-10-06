# Dockerfile for "Build & Extract"
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# 1. Install build tools and required Qt libraries (including libxcb-cursor0)
RUN apt-get update && apt-get install -y --no-install-recommends \
    patchelf \
    binutils \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6dbus6 \
    libxkbcommon-x11-0 \
    libgl1 \
    libxcb-cursor0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir pyinstaller

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy source code
COPY . .

# 4. Compile executable using .spec file
RUN pyinstaller --clean -y sfusion.spec