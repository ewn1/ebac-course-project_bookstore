import pytest

# Importamos as fábricas necessárias para construir nossos dublês de teste
from app_product.factories import ProductFactory, CategoryFactory

# Importamos o interpretador que queremos testar
from app_product.serializers.product_serializer import ProductSerializer

# BANCO DE DADOS DE TESTE:
# Esta linha avisa ao pytest que todas as funções deste arquivo vão interagir com
# o banco de dados simulado. Sem isso, o Django barra a criação das Factories.
pytestmark = pytest.mark.django_db


def test_product_serializer_fields_output():
    """
    TESTE DE ESTRUTURA DO PRODUTO (GET)
    Garante que o ProductSerializer está convertendo o modelo Product para um JSON
    correto e completo, incluindo o aninhamento correto das categorias para o React.
    """
    category = CategoryFactory(title="Alta Fantasia", slug="alta-fantasia")
    product = ProductFactory(title="O Silmarillion", price=59.90, category=[category])

    serializer = ProductSerializer(product)
    data = serializer.data

    assert data["id"] == product.id
    assert data["title"] == "O Silmarillion"
    assert float(data["price"]) == 59.90
    assert data["active"] is True
    assert data["category"][0]["title"] == "Alta Fantasia"
    assert data["category"][0]["slug"] == "alta-fantasia"


def test_product_serializer_creation_with_category_ids():
    """
    TESTE DE CRIAÇÃO DO PRODUTO (POST)
    Garante que o nosso método create() customizado recebe uma lista de IDs de
    categorias vindas do Front-end e vincula corretamente ao produto em lote (.set()).
    """
    # 1. Preparação (Arrange): Criamos as categorias no banco fictício
    cat_tolkien = CategoryFactory(title="Universo de Tolkien", slug="tolkien")
    cat_mitologia = CategoryFactory(title="Mitologia", slug="mitologia")

    # Simulamos o JSON de envio que o carrinho/painel do React mandaria no POST
    payload = {
        "title": "Contos Inacabados",
        "description": "Histórias raras da Terra-média",
        "price": 69.90,
        "active": True,
        "category_ids": [cat_tolkien.id, cat_mitologia.id],
    }

    # 2. Execução (Act): Passamos o payload pelo serializer e mandamos salvar
    serializer = ProductSerializer(data=payload)
    assert serializer.is_valid() is True
    product = serializer.save()

    # 3. Verificação (Assert): O produto precisa ter as duas categorias vinculadas
    assert product.title == "Contos Inacabados"
    assert product.category.count() == 2
    assert cat_tolkien in product.category.all()
    assert cat_mitologia in product.category.all()
