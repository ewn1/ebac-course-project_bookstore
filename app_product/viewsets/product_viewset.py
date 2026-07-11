# 1. IMPORTAÇÕES DA VIEWSET DO PRODUTO
# O ModelViewSet gerencia o ciclo completo do CRUD (Create, Read, Update, Delete).
from rest_framework.viewsets import ModelViewSet

# Importamos o Modelo e o Tradutor (Serializer) específicos do produto.
from app_product.models import Product
from app_product.serializers.product_serializer import ProductSerializer


class ProductViewSet(ModelViewSet):
    """
    Controla o ciclo de vida das requisições de Produtos.
    Utiliza uma abordagem dinâmica para buscar os dados no banco.
    """

    # Definimos o tradutor padrão que vai formatar as entradas e saídas de dados.
    serializer_class = ProductSerializer

    # 2. O PULO DO GATO: CONSULTA DINÂMICA
    # Em vez de usar a variável estática 'queryset = Product.objects.all()',
    # sobrescrevemos o método 'get_queryset'.
    def get_queryset(self):
        """
        Este método é executado pelo DRF toda vez que uma requisição chega.
        Ele retorna a lista de registros que a ViewSet deve manipular.
        """
        # Por enquanto, ele faz o básico: retorna todos os produtos do banco.
        return Product.objects.all()
