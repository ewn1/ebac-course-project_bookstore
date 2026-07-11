# 1. FERRAMENTAS DE ROTEAMENTO DO DJANGO E DO DRF
# 'path' cria caminhos comuns, 'include' permite embutir grupos de URLs de outros arquivos.
from django.urls import path, include

# Importamos os 'routers' do DRF, os caras responsáveis por criar URLs automáticas para ViewSets.
from rest_framework import routers

# Importamos o arquivo/módulo onde nossas ViewSets (nossos motores de CRUD) foram criadas.
from app_order import viewsets

# 2. INSTANCIANDO O ROTEADOR
# O 'SimpleRouter' é um gerador automático de rotas padrão.
# Ele vai olhar para a nossa ViewSet e deduzir quais URLs um CRUD precisa ter.
router = routers.SimpleRouter()

# 3. REGISTRANDO A VIEWSET NO ROTEADOR
# Aqui dizemos: "Router, pegue a OrderViewSet e amarre ela ao prefixo 'order'".
# O 'r"order"' define o início da URL (ex: /order/).
# O 'basename="order"' é o nome interno que o Django usa para fazer buscas reversas de URL (reverse('order-list')).
router.register(r"order", viewsets.OrderViewSet, basename="order")

# 4. AS URLSPATNS GERAIS DO APP
urlpatterns = [
    # O 'router.urls' contém uma lista com várias rotas geradas automaticamente (GET, POST, etc.).
    # Com o 'include(router.urls)', injetamos todas elas de uma vez só na raiz ("") deste app.
    path("", include(router.urls)),
]
