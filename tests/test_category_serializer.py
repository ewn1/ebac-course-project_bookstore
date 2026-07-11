import pytest
from app_product.factories import CategoryFactory
from app_product.serializers.category_serializer import CategorySerializer

# BANCO DE DADOS DE TESTE:
# Garante que o pytest consiga interagir com o banco de dados simulado do Django
# para testar a serialização das nossas categorias da Terra-média.
pytestmark = pytest.mark.django_db


def test_category_serializer_fields_output():
    """
    TESTE DE ESTRUTURA DA CATEGORIA (GET)
    Garante que o CategorySerializer converte o modelo Category para um JSON
    correto, completo e com todos os campos necessários para o Front-end do React.
    """
    # 1. Preparação dos Dados (Arrange):
    # Fabricamos uma categoria temática usando a nossa fábrica do Factory Boy.
    category = CategoryFactory(
        title="Contos de Valinor",
        slug="contos-de-valinor",
        description="Livros que narram os dias antigos dos Elfos na terra abençoada.",
        active=True,
    )

    # 2. Execução do Teste (Act):
    # Passamos o objeto do banco pelo interpretador para gerar o dicionário de dados (JSON)
    serializer = CategorySerializer(category)
    data = serializer.data

    # 3. Verificação dos Resultados (Assert):
    # Conferimos se todas as chaves exigidas pelo contrato da API foram geradas perfeitamente.
    assert data["id"] == category.id
    assert data["title"] == "Contos de Valinor"
    assert data["slug"] == "contos-de-valinor"
    assert (
        data["description"]
        == "Livros que narram os dias antigos dos Elfos na terra abençoada."
    )
    assert data["active"] is True


def test_category_serializer_validation():
    """
    TESTE DE VALIDAÇÃO (POST/PUT)
    Garante que o serializer valida os dados recebidos corretamente. Por exemplo,
    se enviarmos dados válidos, ele deve aceitar e nos permitir salvar uma nova categoria.
    """
    # 1. Preparação (Arrange): Criamos os dados que simulariam um formulário de cadastro
    payload = {
        "title": "Poesia Épica",
        "slug": "poesia-epica",
        "description": "Baladas e poemas rimados da Primeira Era.",
        "active": True,
    }

    # 2. Execução (Act): Alimentamos o serializer com o payload bruto
    serializer = CategorySerializer(data=payload)

    # 3. Verificação (Assert): O serializer precisa validar como True
    assert serializer.is_valid() is True

    # Ao salvar, a categoria precisa ser persistida corretamente no banco
    nova_categoria = serializer.save()
    assert nova_categoria.title == "Poesia Épica"
    assert nova_categoria.slug == "poesia-epica"
