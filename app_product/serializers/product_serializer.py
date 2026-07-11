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

    def create(self, validated_data):
        """
        MÉTODO DE CRIAÇÃO CUSTOMIZADA (PRODUTO COM CATEGORIAS)
        Como um produto pode pertencer a múltiplas categorias (ManyToMany), o DRF
        não sabe salvá-lo automaticamente de primeira. Sobrescrevemos o create()
        para isolar as categorias, salvar o produto e depois vincular tudo em lote.
        """

        # 1. ISOLANDO AS CATEGORIAS
        # Removemos a lista de categorias do dicionário para não quebrar o .create() do produto.
        # Buscamos primeiro por "category" (caso use source="category") e depois por "category_ids".
        categories_data = validated_data.pop(
            "category", validated_data.pop("category_ids", [])
        )

        # 2. CRIANDO O PRODUTO (PAI)
        # Com o validated_data limpo, o '**' desempacota os campos (ex: title, price)
        # e cria o registro do Produto diretamente no banco de dados.
        product = Product.objects.create(**validated_data)

        # 3. VINCULANDO AS CATEGORIAS (FILHOS) EM LOTE (PADRÃO DE MERCADO)
        # Em vez de usar um loop 'for' com '.add()' (que faz várias buscas lentas no banco),
        # usamos o '.set()'. Ele injeta todas as categorias de uma vez só na tabela intermediária.
        product.category.set(categories_data)

        # 4. RETORNO DA INSTÂNCIA
        # Devolvemos o produto pronto e integrado para o DRF gerar o JSON de resposta ao React.
        return product
