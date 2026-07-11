import factory

# Importamos os modelos que esta fábrica vai alimentar com dados fictícios para os testes
from app_product.models import Product
from app_product.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    """
    A FÁBRICA DE CATEGORIAS FALSAS
    Gera categorias aleatórias e realistas automaticamente nos testes.
    """

    # O factory.Faker escolhe palavras, slugs e frases aleatórias para simular os dados
    title = factory.Faker("word")
    slug = factory.Faker("slug")
    description = factory.Faker("sentence")

    # O factory.Iterator alterna entre os valores da lista a cada categoria criada.
    # A primeira categoria criada será True (ativa), a segunda False, a terceira True...
    active = factory.Iterator([True, False])

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    """
    A FÁBRICA DE PRODUTOS FALSOS
    Gera produtos fictícios com preços decimais corretos e faz o vínculo com as categorias.
    """

    # Gera um preço decimal realista (ex: até 3 dígitos na esquerda e 2 na direita -> R$ 149.90)
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    title = factory.Faker("word")

    # controle exclusivo aqui:
    # Como a relação é ManyToMany, precisamos esperar o produto ser salvo no banco primeiro
    # para depois injetar as categorias nele através do '@factory.post_generation'.
    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        # Se for apenas uma simulação na memória (build), não faz nada.
        if not create:
            return

        # Se passarmos categorias específicas no teste (ex: ProductFactory(category=[cat1, cat2])):
        if extracted:
            for category in extracted:
                self.category.add(category)
        else:
            # Se o teste não especificou nenhuma categoria,
            # a fábrica cria uma categoria aleatória automaticamente usando a 'CategoryFactory'
            # e vincula a este produto para o teste não rodar sem dados.
            new_category = CategoryFactory()
            self.category.add(new_category)

    class Meta:
        model = Product
