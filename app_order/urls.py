# 1. FERRAMENTAS DE ROTEAMENTO DO DJANGO E DO DRF
from django.urls import path, include

# Importamos os 'routers' do DRF, os caras responsáveis por criar URLs automáticas para ViewSets.
from rest_framework import routers

# Importamos o arquivo/módulo onde nossas ViewSets foram criadas.
from app_order import viewsets

# 2. INSTANCIANDO O ROTEADOR
router = routers.SimpleRouter()

# =========================================================================
# 3. REGISTRANDO A VIEWSET NO PADRÃO REST (PLURAL)
# =========================================================================
# Seguindo o padrão sênior, alteramos o prefixo de r"order" para r"orders".
# O 'basename="order"' continua igual para manter compatibilidade com as
# buscas reversas internas do Django (ex: reverse('order-list')).
#
# URLs resultantes:
# -> GET /api/v1/orders/ (Lista todos os pedidos)
# -> POST /api/v1/orders/ (Cria um novo pedido)
# =========================================================================
router.register(r"orders", viewsets.OrderViewSet, basename="order")

# 4. AS URLSPATNS GERAIS DO APP
urlpatterns = [
    # Injeta todas as rotas automáticas geradas pelo SimpleRouter na raiz do app.
    path("", include(router.urls)),
]
