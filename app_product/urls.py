# 1. FERRAMENTAS DE ROTEAMENTO DO DJANGO E DO DRF
# 'path' cria os caminhos de URL, 'include' permite embutir grupos de rotas de outros arquivos.
from django.urls import path, include

# Importamos os 'routers' do DRF, responsáveis por gerar as URLs automáticas das ViewSets.
from rest_framework import routers

# Importamos o arquivo/módulo onde nossas ViewSets de produto foram criadas.
from app_product import viewsets

# 2. INSTANCIANDO O ROTEADOR LOCAL
# Usamos o 'SimpleRouter' aqui no submódulo para isolar o escopo do app_product,
# garantindo que ele gere apenas as rotas cruciais do CRUD sem poluir o sistema central.
router = routers.SimpleRouter()

# 3. REGISTRANDO A VIEWSET DE PRODUTOS NO ROTEADOR
# Aqui dizemos: "Router, pegue a ProductViewSet e amarre ela ao prefixo 'product'".
# O 'r"product"' define o início da URL no navegador (ex: /product/).
# O 'basename="product"' cria o nome interno para buscas reversas de URL (ex: reverse('product-list')).
router.register(r"product", viewsets.ProductViewSet, basename="product")

# 4. AS URLSPATNS GERAIS DO APP DE PRODUTOS
urlpatterns = [
    # O 'router.urls' contém o pacote com as 5 rotas padrão geradas automaticamente (GET, POST, etc.).
    # Com o 'include(router.urls)', injetamos todas elas de uma vez só na raiz ("") deste arquivo.
    path("", include(router.urls)),
]
