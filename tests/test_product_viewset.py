import json
import pytest
from django.urls import reverse
from django.contrib.auth.models import (
    User,
)  # Importa o modelo de usuário padrão do Django para os testes
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import (
    Token,
)  # Importa o modelo de Token do Django REST Framework
from app_product.factories import ProductFactory, CategoryFactory
from app_product.models import Product

# =========================================================================
# CONFIGURAÇÃO DE FIXTURES (AMBIENTE DE TESTE)
# =========================================================================


@pytest.fixture
def client():
    """Retorna um cliente de API padrão e anônimo."""
    return APIClient()


@pytest.fixture
def authenticated_client():
    """
    Fixture customizada para gerar um cliente de API já autenticado.

    O que ela faz nos bastidores:
    1. Cria um usuário fictício no banco de dados de testes.
    2. Gera um Token de autenticação atrelado a esse usuário.
    3. Injeta as credenciais (cabeçalho HTTP) no cliente de testes.
    """
    client = APIClient()
    # Cria o usuário que será o "dono" do token
    user = User.objects.create_user(
        username="usuario_teste", password="senha_segura_123"
    )
    # Instancia um token válido para esse usuário
    token = Token.objects.create(user=user)

    # Injeta de forma global o cabeçalho 'Authorization: Token <key>' nas requisições deste cliente
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


# =========================================================================
# CLASSES DE TESTE DO VIEWSET
# =========================================================================


@pytest.mark.django_db  # Avisa ao Pytest que estes testes vão interagir com o banco de dados
class TestProductViewSet:

    def test_get_all_products_from_fantasy_universes(self, authenticated_client):
        """
        Testa a listagem (GET) de produtos vindos de diferentes categorias.
        Agora utiliza o 'authenticated_client' para evitar o erro 403 (Forbidden).
        """
        # --- PASSO 1: Preparação dos Dados (Arrange) ---
        # Usamos o FactoryBoy para simular os registros que estariam no banco de dados
        cat_tolkien = CategoryFactory(title="Universo de Tolkien")
        cat_witcher = CategoryFactory(title="Universo de The Witcher")
        cat_narnia = CategoryFactory(title="As Crônicas de Nárnia")

        # Vinculamos as categorias criadas acima diretamente na lista 'category' do produto
        ProductFactory(
            title="O Senhor dos Anéis: A Sociedade do Anel",
            price=59.90,
            category=[cat_tolkien],
        )
        ProductFactory(title="O Último Desejo", price=49.90, category=[cat_witcher])
        ProductFactory(
            title="O Leão, a Feiticeira e o Guarda-Roupa",
            price=39.90,
            category=[cat_narnia],
        )

        # --- PASSO 2: Execução da Ação (Act) ---
        # O 'reverse' resolve dinamicamente a rota nomeada 'product-list' injetando o parâmetro da versão URL
        url = reverse("product-list", kwargs={"version": "v1"})
        response = authenticated_client.get(url)  # Faz o disparo do método GET

        # --- PASSO 3: Validação dos Resultados (Assert) ---
        # 1. Verifica se a API respondeu Sucesso (200 OK)
        assert response.status_code == status.HTTP_200_OK

        data = response.data

        # 2. Como a rota possui paginação ativa, os dados reais ficam dentro da chave 'results'
        assert len(data["results"]) == 3

        # Cria uma lista apenas com os títulos retornados pela resposta da API usando List Comprehension
        titles = [product["title"] for product in data["results"]]

        # 3. Garante que todos os produtos que criamos no Passo 1 estão presentes na resposta da API
        assert "O Senhor dos Anéis: A Sociedade do Anel" in titles
        assert "O Último Desejo" in titles
        assert "O Leão, a Feiticeira e o Guarda-Roupa" in titles

    def test_create_product_of_tolkien(self, authenticated_client):
        """
        Testa a criação (POST) de um novo produto via API.
        Garante que a autenticação permite a escrita e que o registro é devidamente persistido.
        """
        # --- PASSO 1: Preparação dos Dados (Arrange) ---
        cat_tolkien = CategoryFactory(title="Universo de Tolkien")
        url = reverse("product-list", kwargs={"version": "v1"})

        # Montamos o dicionário com o payload simulando o JSON enviado por um cliente frontend
        data = {
            "title": "O Silmarillion",
            "price": "69.90",
            "category_ids": [
                cat_tolkien.id
            ],  # Passamos o ID da categoria criada pelo factory
            "active": True,
        }

        # --- PASSO 2: Execução da Ação (Act) ---
        # Faz o disparo do método POST. Convertemos o dicionário em string JSON usando 'json.dumps'
        # e explicitamos que o conteúdo é do tipo 'application/json'
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # --- PASSO 3: Validação dos Resultados (Assert) ---
        # 1. Verifica se a API retornou o status de criação correto (201 Created)
        assert response.status_code == status.HTTP_201_CREATED

        # 2. Valida se o corpo da resposta traz os mesmos dados do produto recém-criado
        assert response.data["title"] == "O Silmarillion"

        # 3. Teste de Caixa Preta/Banco de Dados: Garante que o Django de fato salvou o registro no banco
        assert Product.objects.filter(title="O Silmarillion").exists()
