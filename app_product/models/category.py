from django.db import models


class Category(models.Model):
    """
    O MODELO DE CATEGORIAS (CATEGORY)
    Esta tabela serve para organizar os produtos do seu e-commerce.
    Na WeePaper&3D, você poderia ter categorias como: "Impressões 3D", "Papelaria", "Action Figures", etc.
    """

    # O nome visível da categoria (ex: "Impressões 3D")
    title = models.CharField(max_length=100)

    # SLUG: É a versão do título amigável para URLs da web (ex: de "Impressões 3D" vira "impressoes-3d").
    # O 'unique=True' garante que não existirão duas categorias com a mesma URL.
    slug = models.SlugField(unique=True)

    # Uma breve descrição da categoria.
    # 'blank=True' permite que o painel admin deixe o campo vazio.
    # 'null=True' diz ao banco de dados que essa coluna pode guardar valores nulos (vazios).
    description = models.CharField(max_length=200, blank=True, null=True)

    # Campo booleano para desativar ou ativar uma categoria inteira no site sem precisar deletá-la.
    active = models.BooleanField(default=True)

    # o def __str__(self) é um método especial do Python que define como o objeto será representado em formato de texto.
    def __str__(self):
        """
        Esta função define a representação do objeto em formato de texto.
        Quando você olhar essa categoria no Django Admin ou der um print nela no terminal,
        o Django vai exibir o título dela (ex: 'Papelaria') em vez de 'Category object (1)'.
        """
        return self.title
