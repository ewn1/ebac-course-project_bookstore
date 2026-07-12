# 1. FERRAMENTAS DE ROTEAMENTO DO DJANGO E DO DRF
from django.urls import path, include

# Importamos os 'routers' do DRF, responsáveis por gerar as URLs automáticas das ViewSets.
from rest_framework import routers

# Importamos o arquivo/módulo onde nossas ViewSets de produto foram criadas.
from app_product import viewsets

# 2. INSTANCIANDO O ROTEADOR LOCAL
router = routers.SimpleRouter()

# =========================================================================
# 3. REGISTRANDO A VIEWSET NO PADRÃO REST (PLURAL)
# =========================================================================
# Mudamos o prefixo de r"product" para r"products".
# Em APIs profissionais, coleções de dados são sempre representadas no plural.
# Isso evita a repetição feia de '/product/v1/product/' e transforma em:
# -> GET /api/v1/products/ (Lista todos os produtos)
# -> GET /api/v1/products/3/ (Busca o produto de ID 3)
# =========================================================================
router.register(r"products", viewsets.ProductViewSet, basename="product")

# 4. AS URLSPATNS GERAIS DO APP DE PRODUTOS
urlpatterns = [
    # O 'router.urls' injeta na raiz deste arquivo as rotas do CRUD de produtos.
    # Como a string está vazia "", ela se anexa diretamente ao '/api/v1/' central.
    path("", include(router.urls)),
]
