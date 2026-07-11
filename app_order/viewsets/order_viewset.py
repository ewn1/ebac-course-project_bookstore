# 1. O MOTOR DE CRUD AUTOMÁTICO DO DRF
# Importamos o ModelViewSet. Ele é uma classe "combo" do Django Rest Framework
# que já vem com toda a lógica de banco de dados (CRUD) pronta para uso.
from rest_framework.viewsets import ModelViewSet

# 2. AS MATÉRIAS-PRIMAS DA NOSSA VIEW
# Precisamos do Modelo (para saber de qual tabela do banco ler/gravar os dados)
# e do Serializer (o tradutor que transforma os dados do banco em JSON e vice-versa).
from app_order.models import Order
from app_order.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    """
    Esta classe controla todas as requisições HTTP (GET, POST, PUT, PATCH, DELETE)
    relacionadas aos Pedidos (Orders), sem precisarmos escrever cada método na mão.
    """

    # O SERIALIZER_CLASS diz ao Django qual "tradutor" usar para validar os dados
    # recebidos no POST/PUT e para formatar a resposta que volta em JSON.
    serializer_class = OrderSerializer

    # 3. O PULO DO GATO: CONSULTA DINÂMICA (BOA PRÁTICA DE MERCADO)
    # Em vez de usar a variável estática 'queryset = Order.objects.all()',
    # sobrescrevemos o método 'get_queryset'. Isso protege nossa API e permite
    # aplicar lógicas futuras (como fazer o cliente ver apenas os seus próprios pedidos).
    def get_queryset(self):
        """
        Este método é executado pelo DRF toda vez que uma requisição chega.
        Ele define o "escopo" inicial de quais registros do banco de dados
        esta ViewSet pode manipular.
        """
        # Por enquanto, ele faz a busca geral trazendo todos os pedidos.
        # A consulta só vai de fato ao banco de dados no momento da requisição!
        return Order.objects.all()
