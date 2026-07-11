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
        Usamos a agregação nativa do banco de dados para somar os valores.
        Isso evita carregar dezenas de objetos na memória do servidor,
        tornando a API extremamente rápida mesmo com carrinhos gigantes.
        """
        from django.db.models import Sum

        # Pedimos para o banco de dados somar a coluna 'price' e retornar o resultado.
        # O '|| 0' (ou o .get('price__sum') or 0) garante que se o carrinho estiver vazio, o total seja 0.
        dados_soma = instance.product.aggregate(Sum("price"))
        return dados_soma.get("price__sum") or 0

    class Meta:
        model = Order

        # Expandimos os campos para o seu e-commerce ficar completo e profissional:
        # Incluímos o 'id' do pedido, o 'user' comprador e o canal de envio 'product_ids'.
        fields = ["id", "user", "product", "product_ids", "total"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        MÉTODO DE CRIAÇÃO CUSTOMIZADA (GRAVAÇÃO EM TABELAS RELACIONADAS)
        Por padrão, o DRF não sabe como salvar um Pedido que tem uma lista de
        Produtos dentro (relação ManyToMany). Sobrescrevemos o método create()
        para ensinar o Django a separar o Pedido dos Produtos na hora de salvar.
        """

        # 1. ISOLANDO OS PRODUTOS
        # O React envia uma lista de IDs de produtos dentro do campo "product".
        # Usamos o .pop() para "arrancar" essa lista de dentro do dicionário validated_data.
        # Fazemos isso porque o método Order.objects.create() não aceita uma lista de cara.
        # O segundo argumento [] é uma segurança: se não vier produto nenhum, ele assume uma lista vazia.
        products_data = validated_data.pop("product", [])

        # 2. CRIANDO O PEDIDO (PAI)
        # Agora que o dicionário validated_data está limpo (sem a lista de produtos),
        # usamos os dois asteriscos (**) para desempacotar o dicionário (ex: user=user_id).
        # Isso cria o registro do Pedido no banco de dados e nos devolve a instância 'order'.
        order = Order.objects.create(**validated_data)

        # 3. VINCULANDO OS FILHOS (PRODUTOS) AO PEDIDO
        # Com o pedido já criado e com um ID gerado pelo banco, usamos o método .set().
        # O .set() recebe a lista de IDs de produtos e faz o vínculo automático deles
        # com o pedido na tabela intermediária do banco de dados de forma ultra performática.
        order.product.set(products_data)

        # 4. RETORNO DA INSTÂNCIA
        # Devolvemos o pedido completo e devidamente vinculado para a ViewSet responder o JSON ao Front-end.
        return order
