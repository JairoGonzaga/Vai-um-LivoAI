# ============================================================
#  Dockerfile — LivroAI
#  Hugging Face Spaces (Docker)
# ============================================================

FROM python:3.11-slim

# ----------------------------------------------------------
# Usuário não-root — obrigatório no HF Spaces
# ----------------------------------------------------------
RUN useradd -m -u 1000 user
USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# ----------------------------------------------------------
# Dependências do sistema necessárias para o ultralytics
# ----------------------------------------------------------
USER root
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
USER user

# ----------------------------------------------------------
# Instala dependências Python
# ----------------------------------------------------------
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------------
# Copia o projeto
# ----------------------------------------------------------
COPY --chown=user . .

# ----------------------------------------------------------
# Porta obrigatória do HF Spaces
# ----------------------------------------------------------
EXPOSE 7860

# ----------------------------------------------------------
# Inicia o servidor
# ----------------------------------------------------------
CMD ["uvicorn", "app.core.main:app", "--host", "0.0.0.0", "--port", "7860"]