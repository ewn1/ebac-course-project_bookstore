# 1. IMPORTAÇÕES DA VIEWSET DO PRODUTO
# O ModelViewSet gerencia o ciclo completo do CRUD (Create, Read, Update, Delete).
from rest_framework.viewsets import ModelViewSet

# Importamos o Modelo e o Tradutor (Serializer) específicos do produto.
from app_product.models import Product
from app_product.serializers.product_serializer import ProductSerializer

# Importamos as classes de Autenticação (como o usuário prova quem ele é).
# SessionAuthentication: Usa a sessão do navegador (cookies) - ótimo para testes no browser e painel admin.
# BasicAuthentication: Usa cabeçalho HTTP com usuário e senha - bom para testes via Postman/Insomnia.
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)

# Importamos as classes de Permissão (o que o usuário autenticado tem autorização para fazer).
# IsAuthenticated: Bloqueia o acesso de visitantes anônimos. Só entra quem estiver logado.
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(ModelViewSet):
    """
    Controla o ciclo de vida das requisições de Produtos.
    Utiliza uma abordagem dinâmica para buscar os dados no banco.
    """

    # 2. SEGURANÇA DA VIEWSET
    # authentication_classes: Define os métodos aceitos para reconhecer o usuário da requisição.
    # O DRF vai tentar validar a Sessão; se não encontrar, tenta validar via Basic Auth.
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication,
    ]

    # permission_classes: Define a barreira de acesso.
    # Aqui dizemos: "Para acessar qualquer endpoint de Produto (GET, POST, etc),
    # você TEM que ser um usuário reconhecido/logado."
    permission_classes = [IsAuthenticated]

    # Definimos o tradutor padrão que vai formatar as entradas e saídas de dados.
    serializer_class = ProductSerializer

    # 3. O PULO DO GATO: CONSULTA DINÂMICA
    # Em vez de usar a variável estática 'queryset = Product.objects.all()',
    # sobrescrevemos o método 'get_queryset'.
    def get_queryset(self):
        """
        Este método é executado pelo DRF toda vez que uma requisição chega.
        Ele retorna a lista de registros que a ViewSet deve manipular.
        """
        # Por enquanto, ele faz o básico: retorna todos os produtos do banco.
        return Product.objects.all()
