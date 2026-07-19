# --------------------------------------------------------------------------------
# Stage 1: Configuração do ambiente e variáveis globais
# --------------------------------------------------------------------------------
FROM python:3.12-slim AS python-base

# Configurações para otimizar o Python dentro do container
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Atualizado para a versão estável mais recente do Poetry 2.x
    POETRY_VERSION=2.4.1 \
    POETRY_HOME="/opt/poetry" \
    # SOLUÇÃO REAL: Desativamos a criação de virtualenv dentro do container
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Adiciona apenas o Poetry no PATH do sistema (não precisamos mais do .venv/bin)
ENV PATH="$POETRY_HOME/bin:$PATH"

# --------------------------------------------------------------------------------
# Stage 2: Instalação de dependências do sistema e do Poetry
# --------------------------------------------------------------------------------
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalação moderna do Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# --------------------------------------------------------------------------------
# Stage 3: Instalação do App Django com Poetry 2.4
# --------------------------------------------------------------------------------
WORKDIR /app

# Copia os arquivos de configuração primeiro para aproveitar o cache do Docker
COPY poetry.lock pyproject.toml /app/

# O TRUQUE DE MESTRE: Remove o lock antigo se houver, gera um novo com Poetry 2.4 
# e instala tudo direto no escopo global do container de forma limpa.
RUN rm -f poetry.lock \
    && poetry lock --regenerate \
    && poetry install --no-root --no-interaction --no-ansi

# Copia o restante do código fonte do Django
COPY . /app/

EXPOSE 8000

# Executa as migrations automaticamente antes de subir o servidor (Garante o log limpo!)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]