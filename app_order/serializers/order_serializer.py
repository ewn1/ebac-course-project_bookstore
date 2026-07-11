from rest_framework import serializers

# Importamos o modelo correto de Pedidos (Order) que o professor esqueceu de referenciar na Meta class
from app_order.models import Order
from app_product.models import Product
from app_product.serializers.product_serializer import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    O INTÉRPRETE DE PEDIDOS (ORDER)
    Esta classe traduz o pedido do banco de dados para o Front-end (JSON) e vice-versa.
    Aqui corrigimos o bug do modelo e estruturamos a forma correta de listagem e criação.
    """

    # MODO LEITURA (Para o Front-end listar):
    # Quando o React pedir os dados, o Django vai usar o ProductSerializer para trazer
    # os detalhes completos dos produtos (id, título, preço) em formato de lista (many=True).
    product = ProductSerializer(many=True, read_only=True)

    # MODO ESCRITA (Para o Front-end criar o pedido):
    # Canal oculto para o carrinho do React enviar apenas uma lista de IDs [1, 3, 5].
    # O DRF valida se esses produtos existem e os vincula ao pedido na tabela ManyToMany.
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",  # Alimenta diretamente o campo 'product' do modelo Order
        many=True,
        write_only=True,
    )

    # CAMPO CALCULADO (SerializerMethodField):
    # Este campo não existe fisicamente na tabela do banco de dados.
    # Ele é calculado em "tempo de execução" toda vez que a API gera o JSON.
    total = serializers.SerializerMethodField()

    def get_total(self, instance):
        """
        O CÁLCULO DO VALOR TOTAL DO PEDIDO
        A palavra 'instance' representa o pedido atual que está sendo processado.
        """
        # 1. 'instance.product.all()' busca todos os produtos vinculados a este pedido no banco.
        # 2. O List Comprehension extrai o '.price' de cada um deles.
        # 3. A função 'sum()' soma todos esses preços e retorna o valor final da compra.
        total = sum([product.price for product in instance.product.all()])
        return total

    class Meta:
        # CORREÇÃO: O modelo alvo deste serializer é Order, e não Product!
        model = Order

        # Expandimos os campos para o seu e-commerce ficar completo e profissional:
        # Incluímos o 'id' do pedido, o 'user' comprador e o canal de envio 'product_ids'.
        fields = ["id", "user", "product", "product_ids", "total"]
        read_only_fields = ["id"]
