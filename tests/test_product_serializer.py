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
    TESTE DE ESTRUTURA DO PRODUTO
    Garante que o ProductSerializer está convertendo o modelo Product para um JSON
    correto e completo, incluindo o aninhamento correto das categorias para o React.
    """
    # 1. Preparação dos Dados (Arrange):
    # Fabricamos uma categoria de livro e um produto associado a ela usando dados de Tolkien.
    category = CategoryFactory(title="Alta Fantasia", slug="alta-fantasia")
    product = ProductFactory(title="O Silmarillion", price=59.90, category=[category])

    # 2. Execução do Teste (Act):
    # Passamos o nosso produto fictício pelo Serializer para gerar o JSON final (.data)
    serializer = ProductSerializer(product)
    data = serializer.data

    # 3. Verificação dos Resultados (Assert):
    # Checamos linha por linha se o intérprete gerou as chaves e valores esperados para o Front-end.
    assert data["id"] == product.id
    assert data["title"] == "O Silmarillion"

    # Convertemos para float porque o DecimalField envia o preço como String no JSON por segurança.
    assert float(data["price"]) == 59.90
    assert data["active"] is True

    # Testamos se o relacionamento aninhado funcionou perfeitamente
    assert data["category"][0]["title"] == "Alta Fantasia"
    assert data["category"][0]["slug"] == "alta-fantasia"
