import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import (
    Token,
)  # Importa o modelo de tokens para simular a autenticação do cliente
from app_product.factories import ProductFactory, CategoryFactory
from app_order.factories import OrderFactory, UserFactory
from app_order.models import Order

# =========================================================================
# CONFIGURAÇÃO DE FIXTURES (AMBIENTE DE TESTE AUTENTICADO)
# =========================================================================


@pytest.fixture
def client():
    """Retorna um cliente de API padrão e anônimo (caso precise testar negação de acesso)."""
    return APIClient()


@pytest.fixture
def authenticated_user():
    """Fixture para criar um usuário fixo no banco de dados de teste."""
    return UserFactory(username="usuario_logado")


@pytest.fixture
def authenticated_client(authenticated_user):
    """
    Fixture que monta um cliente HTTP já logado com o 'authenticated_user'.
    Qualquer requisição feita por esse cliente será interpretada pelo Django
    como se o 'usuario_logado' estivesse executando a ação.
    """
    client = APIClient()
    # Cria o token atrelado ao usuário gerado pela fixture acima
    token = Token.objects.create(user=authenticated_user)
    # Injeta a credencial no cliente
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


# =========================================================================
# CLASSES DE TESTE DO VIEWSET DE PEDIDOS
# =========================================================================


@pytest.mark.django_db  # Habilita o acesso ao banco de dados virtual de testes do Django
class TestOrderViewSet:

    def test_get_orders_list(self, authenticated_client, authenticated_user):
        """
        Testa a listagem (GET) de pedidos.
        Garante que a API retorna os pedidos que pertencem ao usuário autenticado.
        """
        # --- PASSO 1: Preparação dos Dados (Arrange) ---
        cat_tolkien = CategoryFactory(title="Universo de Tolkien")

        # Criamos dois produtos fictícios no banco usando os factories do app_product
        book_1 = ProductFactory(title="O Hobbit", price=45.00, category=[cat_tolkien])
        book_2 = ProductFactory(
            title="As Duas Torres", price=55.00, category=[cat_tolkien]
        )

        # REGRA DE OURO DA ALTERAÇÃO: Criamos o pedido apontando diretamente para o
        # 'authenticated_user'. Como a Viewset agora filtra por usuário logado, se criássemos
        # o pedido para outro usuário, a resposta do GET viria vazia!
        order = OrderFactory(user=authenticated_user)

        # Como a relação entre Order e Product é ManyToMany (Muitos para Muitos),
        # usamos o método '.set()' para associar a lista de livros a este pedido.
        order.product.set([book_1, book_2])

        # --- PASSO 2: Execução da Ação (Act) ---
        # O reverse busca a URL registrada como 'order-list' (mapeada no roteador do Django)
        url = reverse("order-list", kwargs={"version": "v1"})
        response = authenticated_client.get(url)  # Envia a requisição GET autenticada

        # --- PASSO 3: Validação dos Resultados (Assert) ---
        # 1. Verifica se fomos autorizados com sucesso (200 OK)
        assert response.status_code == status.HTTP_200_OK

        data = response.data

        # 2. Verifica se a paginação retornou exatamente 1 pedido na lista 'results'
        assert len(data["results"]) == 1

        # 3. Garante que o ID do usuário dono do pedido retornado corresponde ao ID do nosso usuário logado
        assert data["results"][0]["user"] == authenticated_user.id

    def test_create_order_with_witcher_and_narnia_books(
        self, authenticated_client, authenticated_user
    ):
        """
        Testa a criação (POST) de um pedido na API.
        Garante que o envio do JSON correto cria um registro real no banco de dados.
        """
        # --- PASSO 1: Preparação dos Dados (Arrange) ---
        cat_fantasia = CategoryFactory(title="Fantasia")

        book_1 = ProductFactory(
            title="O Sangue dos Elfos", price=50.00, category=[cat_fantasia]
        )
        book_2 = ProductFactory(
            title="O Príncipe Caspian", price=40.00, category=[cat_fantasia]
        )

        url = reverse("order-list", kwargs={"version": "v1"})

        # Montamos o payload. Vinculamos a compra ao ID do usuário autenticado no sistema.
        data = {"user": authenticated_user.id, "product_ids": [book_1.id, book_2.id]}

        # --- PASSO 2: Execução da Ação (Act) ---
        # Disparamos o POST convertendo o dicionário acima em uma string JSON limpa
        response = authenticated_client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # --- PASSO 3: Validação dos Resultados (Assert) ---
        # 1. Verifica se o status retornado foi de criação bem-sucedida (201 Created)
        assert response.status_code == status.HTTP_201_CREATED

        # 2. Validação de Banco de Dados: Garante que a Order foi inserida no banco atrelada a este usuário
        assert Order.objects.filter(user=authenticated_user).exists()

        # 3. Validação de Regra de Negócio: O total retornado pelo Serializer (50.00 + 40.00) deve ser exatamente 90.00
        assert float(response.data["total"]) == 90.00
