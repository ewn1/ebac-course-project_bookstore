# 1. O MOTOR DE CRUD AUTOMÁTICO DO DRF
# Importamos o ModelViewSet. Ele é uma classe "combo" do Django Rest Framework
# que já vem com toda a lógica de banco de dados (CRUD) pronta para uso.
from rest_framework.viewsets import ModelViewSet

# 2. ACESSANDO O SISTEMA DE AUTENTICAÇÃO E PERMISSÕES
# Importamos a classe IsAuthenticated para garantir que apenas usuários que
# enviaram um Token válido consigam interagir com os pedidos da nossa API.
from rest_framework.permissions import IsAuthenticated

# 3. AS MATÉRIAS-PRIMAS DA NOSSA VIEW
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

    # BLINDAGEM DE SEGURANÇA: Nenhuma requisição (seja GET ou POST) passará daqui
    # sem um Token de Autenticação válido no cabeçalho HTTP. Devolve 403 Forbidden caso falhe.
    permission_classes = [IsAuthenticated]

    # 4. CONSULTA DINÂMICA COMPLETA (PADRÃO DE MERCADO REQUERIDO EM EMPRESAS)
    # Sobrescrevemos o método 'get_queryset' para injetar uma regra essencial de negócio:
    # Um cliente NUNCA pode ver, listar ou editar os pedidos feitos por outro cliente!
    def get_queryset(self):
        """
        Este método é executado pelo DRF toda vez que uma requisição chega.
        Filtramos os pedidos dinamicamente capturando quem disparou a requisição.
        """
        # self.request.user contém a instância do usuário que foi autenticado pelo Token.
        # Ordenamos por '-id' (decrescente) para resolver o aviso 'UnorderedObjectListWarning' no Pytest.
        return Order.objects.filter(user=self.request.user).order_by("-id")
