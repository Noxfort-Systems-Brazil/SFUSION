# Dockerfile for SFusion Mapper GUI Application
FROM python:3.12-slim-bookworm

WORKDIR /app

# 1. Install required Qt libraries and X11 dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6dbus6 \
    libxkbcommon-x11-0 \
    libgl1 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Copy source code
COPY . .

# 4. Run application
CMD ["python", "sfusion.py"]