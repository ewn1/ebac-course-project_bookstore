# 1. IMPORTAÇÕES DA VIEWSET DO PRODUTO
from rest_framework.viewsets import ModelViewSet

# Importamos o Modelo e o Tradutor (Serializer) específicos do produto.
from app_product.models import Product
from app_product.serializers.product_serializer import ProductSerializer

# Importamos a classe de Permissão.
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    """
    Controla o ciclo de vida das requisições de Produtos.
    Utiliza uma abordagem dinâmica para buscar os dados no banco.
    """

    # 2. SEGURANÇA DA VIEWSET
    # Exige que o usuário esteja autenticado (usando a autenticação padrão global do settings.py)
    permission_classes = [IsAuthenticated]

    # Definimos o tradutor padrão que vai formatar as entradas e saídas de dados.
    serializer_class = ProductSerializer

    # 3. CONSULTA DINÂMICA
    def get_queryset(self):
        """
        Retorna a lista de registros que a ViewSet deve manipular.
        """
        return Product.objects.all()
