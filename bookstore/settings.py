import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# 1. SEGURANÇA E AMBIENTE (Variáveis de Ambiente para Produção/Docker)
# ==============================================================================
# ATENÇÃO: As linhas originais de SECRET_KEY, DEBUG e ALLOWED_HOSTS que ficavam aqui
# no topo foram sobrescritas no final do arquivo para usar 'os.environ.get'.
# Isso serve para ler os dados do arquivo '.env' através do Docker, impedindo que
# senhas e chaves secretas fiquem expostas no código do GitHub.


# ==============================================================================
# 2. DEFINIÇÃO DE APLICATIVOS (INSTALLED_APPS)
# ==============================================================================
INSTALLED_APPS = [
    # Aplicativos nativos do Django (Gerenciamento, Autenticação, Sessões, etc.)
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # --- ADICIONADOS ALÉM DO PADRÃO ---
    "rest_framework",  # Ativa o Django REST Framework para criar a API.
    "app_order",  # Seu app customizado que gerencia os pedidos.
    "app_product",  # Seu app customizado que gerencia os produtos (livros).
    "django_extensions",  # Canivete suíço com comandos extras para o terminal (ex: shell_plus).
    "debug_toolbar",  # Painel visual no navegador para analisar performance e queries de banco.
    "rest_framework.authtoken",  # Ativa o sistema de autenticação por Token na API (essencial para mobile/frontend).
]


# ==============================================================================
# 3. MIDDLEWARES (Filtros de Requisição/Resposta)
# ==============================================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # --- ADICIONADO ALÉM DO PADRÃO ---
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Intercepta as requisições para renderizar a barra de debug na tela.
]

ROOT_URLCONF = "bookstore.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookstore.wsgi.application"


# ==============================================================================
# 4. BANCO DE DADOS (Configuração Dinâmica para PostgreSQL / Docker)
# ==============================================================================
# Modificado para alternar dinamicamente: se o Docker estiver rodando, ele puxa as
# variáveis do Postgres (SQL_ENGINE, SQL_HOST, etc.). Se não achar nada, ele usa o SQLite local de fallback.
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"


# ===================================================================================
# 5. CONFIGURAÇÕES ADICIONADAS NO FINAL DO ARQUIVO (Customizações da API e Segurança)
# ===================================================================================

# Configurações globais do Django REST Framework (DRF)
REST_FRAMEWORK = {
    # Paginação: Divide as listas da API em páginas para não sobrecarregar o banco.
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,  # Mostra no máximo 5 produtos por página.
    # Classes de Autenticação: Define os métodos aceitos para provar quem é o usuário.
    # Foi o que gerou o erro '403 Forbidden' quando você tentou acessar deslogado.
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",  # Usuário/Senha básicos nos headers.
        "rest_framework.authentication.SessionAuthentication",  # Autenticação por sessão de navegador (usada pelo Admin).
        "rest_framework.authentication.TokenAuthentication",  # Autenticação via Token gerado para o usuário (padrão de mercado para APIs).
    ],
}

# IPs autorizados a ver a 'django-debug-toolbar'. Como rodamos local, o localhost está liberado.
INTERNAL_IPS = ["127.0.0.1"]

# PROTEÇÃO DE AMBIENTE: Sobrescreve as variáveis do topo do arquivo coletando do '.env' via Docker.
SECRET_KEY = os.environ.get("SECRET_KEY")

# Converte o DEBUG para inteiro (0 ou 1) vindo do .env. 0 vira False (Produção), 1 vira True (Desenvolvimento).
DEBUG = int(os.environ.get("DEBUG", default=0))

# Coleta a string de hosts permitidos do .env (ex: "localhost 127.0.0.1") e quebra em uma lista do Python ['localhost', '127.0.0.1']
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
