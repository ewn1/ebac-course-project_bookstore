import pytest
from app_product.factories import ProductFactory
from app_order.factories import OrderFactory
from app_order.serializers.order_serializer import OrderSerializer

# Permite o acesso ao banco de dados fictício para criar os pedidos e usuários de teste
pytestmark = pytest.mark.django_db


def test_order_serializer_calculates_total_correctly():
    """
    TESTE DE LÓGICA DE NEGÓCIO (SOMA DO PEDIDO)
    Garante que o OrderSerializer está calculando o valor total do carrinho
    corretamente através do método que corrige o preço de todos os livros inseridos.
    """
    # 1. Preparação dos Dados (Arrange):
    # Fabricamos dois livros clássicos com preços bem definidos na nossa "Bookstore".
    product1 = ProductFactory(
        title="O Senhor dos Anéis: A Sociedade do Anel", price=79.90
    )
    product2 = ProductFactory(title="O Hobbit", price=45.00)

    # Criamos o pedido e jogamos os dois livros dentro dele (relação ManyToMany)
    order = OrderFactory(product=[product1, product2])

    # 2. Execução do Teste (Act):
    # O Serializer intercepta o pedido e calcula o total em tempo de execução
    serializer = OrderSerializer(order)
    data = serializer.data

    # 3. Verificação dos Resultados (Assert):
    # A soma exata de 79.90 + 45.00 precisa dar exatamente 124.90 no campo 'total' do JSON.
    assert float(data["total"]) == 124.90

    # Garantimos que as chaves de identificação do pedido e do usuário também estão corretas
    assert data["id"] == order.id
    assert data["user"] == order.user.id
