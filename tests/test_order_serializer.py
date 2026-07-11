import pytest
from django.contrib.auth.models import User
from app_product.factories import ProductFactory
from app_order.factories import OrderFactory
from app_order.serializers.order_serializer import OrderSerializer
from app_order.models import Order

# Permite o acesso ao banco de dados fictício para criar os pedidos e usuários de teste
pytestmark = pytest.mark.django_db


def test_order_serializer_calculates_total_correctly():
    """
    TESTE DE LÓGICA DE NEGÓCIO (SOMA DO PEDIDO)
    Garante que o OrderSerializer está calculando o valor total do carrinho
    corretamente através da agregação nativa (Sum) direto no banco de dados.
    """
    product1 = ProductFactory(
        title="O Senhor dos Anéis: A Sociedade do Anel", price=79.90
    )
    product2 = ProductFactory(title="O Hobbit", price=45.00)

    order = OrderFactory(product=[product1, product2])

    serializer = OrderSerializer(order)
    data = serializer.data

    assert float(data["total"]) == 124.90
    assert data["id"] == order.id
    assert data["user"] == order.user.id


def test_order_serializer_creation_with_product_ids():
    """
    TESTE DE CRIAÇÃO DE PEDIDO (POST)
    Garante que quando o React envia o carrinho preenchido com IDs de livros,
    o serializer extrai esses IDs (.pop()), cria o pedido e faz o vínculo em lote (.set()).
    """
    # 1. Preparação (Arrange): Precisamos de um usuário comprador e livros na vitrine
    comprador = User.objects.create_user(username="frodo_bolseiro")
    livro_1 = ProductFactory(title="O Retorno do Rei", price=79.90)
    livro_2 = ProductFactory(title="As Duas Torres", price=79.90)

    payload = {
        "user": comprador.id,
        "product_ids": [livro_1.id, livro_2.id],  # IDs simulando o carrinho do Front
    }

    # 2. Execução (Act)
    serializer = OrderSerializer(data=payload)
    assert serializer.is_valid() is True
    order = serializer.save()

    # 3. Verificação (Assert)
    assert order.user == comprador
    assert order.product.count() == 2
    # Garante que nosso método get_total calculou os dois volumes corretamente
    assert float(OrderSerializer(order).data["total"]) == 159.80
