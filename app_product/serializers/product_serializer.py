from rest_framework import serializers
from app_product.models.product import Product

# Importamos o interpretador de categorias para aninhar as informações no JSON
from app_product.serializers.category_serializer import CategorySerializer
from app_product.models.category import Category


class ProductSerializer(serializers.ModelSerializer):
    """
    O INTÉRPRETE DE PRODUTOS (PRODUCT)
    Esta classe traduz os dados dos produtos entre o banco de dados e o formato JSON do Front-end.
    Aqui resolvemos o problema de permitir tanto a leitura detalhada quanto a criação simples por IDs.
    """

    # MODO LEITURA (Para o Front-end renderizar a vitrine):
    # Quando o React pedir o produto, trazemos todos os detalhes da categoria aninhados
    # (id, título, slug) em vez de apenas o número do ID. Colocamos 'read_only=True'.
    category = CategorySerializer(many=True, read_only=True)

    # MODO ESCRITA (Para criar ou atualizar produtos):
    # Canal limpo para o Front-end enviar apenas uma lista com os números dos IDs das categorias
    # no momento do cadastro (ex: [1, 3]). O DRF valida se essas categorias existem e faz o vínculo.
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",  # Vincula diretamente esses IDs ao campo 'category' do modelo Product
        many=True,
        write_only=True,  # Esse campo só serve para receber dados no POST; ele não aparece no JSON final do GET
    )

    class Meta:
        model = Product

        # ADICIONADO: Incluímos o 'id' do próprio produto e o nosso canal de gravação 'category_ids'
        fields = [
            "id",
            "title",
            "description",
            "price",
            "active",
            "category",
            "category_ids",
        ]

        # Garante que o ID do produto é controlado estritamente pelo banco de dados
        read_only_fields = ["id"]
