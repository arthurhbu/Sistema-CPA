FROM python:3.11-slim-bookworm
LABEL maintainer="CPA <cpa@uem.br>"
LABEL br.uem.cpa.sistema.backend.author="Arthur Ueda"

WORKDIR /app

# Instala dependências do sistema necessárias para compilar o pycairo
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    libcairo2-dev \
    python3-dev \
    meson \
    ninja-build \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade $(pip list --outdated | tail -n +3 | awk '{print $1}') || true

COPY . .

EXPOSE 5000

ENTRYPOINT ["python", "-u", "/app/app.py"]
