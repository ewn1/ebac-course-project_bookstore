from django.db import models

# Importamos o modelo Category do mesmo diretório para fazer o relacionamento
from .category import Category


class Product(models.Model):
    """
    O MODELO DE PRODUTOS (PRODUCT)
    Esta é a tabela principal do catálogo do seu e-commerce.
    Na WeePaper&3D, cada linha desta tabela representará um produto físico ou um serviço de impressão.
    """

    # O nome comercial do produto (ex: "Miniatura Darth Vader 15cm")
    title = models.CharField(max_length=100)

    # Campo de texto longo para a descrição detalhada do produto.
    # Usamos 'TextField' em vez de 'CharField' porque ele não tem o limite rígido de caracteres na tela.
    description = models.TextField(max_length=500, blank=True, null=True)

    # (Tratamento de Dinheiro):
    # Substituímos o 'PositiveIntegerField' (que proibia centavos) pelo 'DecimalField'.
    # max_digits=10 -> O número pode ter até 10 dígitos no total (ex: 99.999.999,99)
    # decimal_places=2 -> Garante exatamente duas casas decimais para os centavos (,00)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # Define se o produto está visível/disponível para venda no site ou se foi pausado.
    active = models.BooleanField(default=True)

    # RELAÇÃO MUITOS-PARA-MUITOS (ManyToMany):
    # Um produto pode pertencer a várias categorias ao mesmo tempo (ex: um chaveiro do Star Wars
    # pode estar em "Geek" e também em "Acessórios").
    # 'blank=True' significa que o produto pode ser cadastrado sem nenhuma categoria inicialmente.
    category = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        """
        Retorna o nome do produto ao invés de 'Product object (1)' no painel Admin do Django.
        """
        return self.title
