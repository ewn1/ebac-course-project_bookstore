from rest_framework import serializers

# Importamos o modelo Category que este serializer vai interpretar
from app_product.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    O INTÉRPRETE DE CATEGORIAS (CATEGORY)
    Esta classe ensina o Django REST Framework a transformar os dados da tabela
    Category (Banco de Dados) para o formato JSON (Front-end) e vice-versa.
    """

    class Meta:
        # 1. Indicamos qual o modelo do banco que estamos espelhando
        model = Category

        # 2. Definimos quais campos o Front-end (React) vai receber no JSON.
        #    ADICIONADO: Incluímos o 'id' no início da lista, pois o Front-end
        #    precisa dele como chave única (key) para renderizar listas na tela.
        fields = ["id", "title", "slug", "description", "active"]

        # 3. Garantimos que o ID é gerado apenas pelo banco de dados (Apenas Leitura).
        read_only_fields = ["id"]
