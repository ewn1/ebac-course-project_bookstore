import factory

# Importamos o modelo de Usuário padrão do Django para podermos fabricar usuários falsos nos testes
from django.contrib.auth.models import User

# Importamos a fábrica de produtos do outro app (usada se quisermos linkar produtos reais aos testes)
from app_product.factories import ProductFactory

# Importamos o modelo de Pedido que esta fábrica vai gerar
from app_order.models import Order


class UserFactory(factory.django.DjangoModelFactory):
    """
    A FÁBRICA DE USUÁRIOS FALSOS
    Toda vez que chamarmos 'UserFactory()', essa classe vai gerar um usuário
    com dados aleatórios realistas no banco de dados para os nossos testes automatizados.
    """

    # O 'factory.Faker' usa uma biblioteca de inteligência de dados falsos.
    # Ele gera e-mails e nomes de usuário únicos e aleatórios automaticamente.
    email = factory.Faker("email")
    username = factory.Faker("user_name")

    class Meta:
        model = User  # Dizemos que esta fábrica gera objetos do modelo User


class OrderFactory(factory.django.DjangoModelFactory):
    """
    A FÁBRICA DE PEDIDOS FALSOS
    Esta classe resolve a criação automática de pedidos para os testes, lidando
    com o usuário comprador e a lista de produtos associados.
    """

    # SUBFACTORY (Fábrica Aninhada):
    # Um pedido precisa obrigatoriamente de um usuário. O 'SubFactory' diz ao Django:
    # "Se eu criar um pedido fictício e não passar nenhum usuário, use a 'UserFactory'
    # ali de cima para criar um usuário aleatório na hora e vincular a este pedido."
    user = factory.SubFactory(UserFactory)

    # O PULO DO GATO PARA CAMPOS MUITOS-PARA-MUITOS (ManyToMany):
    # No Django, você não pode adicionar produtos a um pedido antes do pedido existir fisicamente no banco (com um ID).
    # O decorador '@factory.post_generation' diz à fábrica: "Espere o pedido ser salvo no banco primeiro.
    # DEPOIS que ele for criado, rode esta função abaixo para injetar os produtos nele."
    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        # Se for apenas uma simulação na memória (build) e não salvar no banco de dados, não faz nada.
        if not create:
            return

        # Se passarmos uma lista de produtos na hora de criar a fábrica (ex: OrderFactory(product=[prod1, prod2])):
        if extracted:
            for product in extracted:
                # O método '.add()' insere o produto na tabela intermediária ManyToMany do banco de dados
                self.product.add(product)

    class Meta:
        model = Order  # Esta fábrica gera objetos do modelo Order
