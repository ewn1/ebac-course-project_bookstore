from django.db import models

# Importamos o modelo de Usuário padrão do Django para ligar o pedido a um cliente
from django.contrib.auth.models import User


class Order(models.Model):
    """
    O MODELO DE PEDIDOS (ORDER)
    Esta classe define a tabela no banco de dados que guardará os pedidos da loja.
    Ela faz a ponte crucial entre QUEM está comprando (User) e O QUE está sendo comprado (Product).
    """

    # RELAÇÃO MUITOS-PARA-MUITOS (ManyToMany):
    # Um pedido pode ter vários produtos dentro dele, e um produto pode estar em vários pedidos diferentes.
    # Usamos o "endereço completo" ('app_product.Product') para evitar erros de importação circular.
    # O Django criará uma tabela intermediária oculta no banco de dados para gerenciar essa união.
    product = models.ManyToManyField("app_product.Product", blank=False)

    # RELAÇÃO CHAVE ESTRANGEIRA (ForeignKey):
    # Vincula o pedido a um usuário específico do sistema. Um usuário pode ter vários pedidos (1 para Muitos).
    # O 'on_delete=models.CASCADE' é uma regra de segurança do banco: se o usuário for deletado do sistema,
    # todos os pedidos associados a ele também serão deletados automaticamente para não deixar dados órfãos.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 💡 ADICIONAL DE MERCADO (Opcional, mas altamente recomendado para e-commerce):
    # Se o professor não colocou estes campos abaixo, você pode adicioná-los para o seu projeto ficar profissional.
    # Eles registram automaticamente a data de criação do pedido e o status atual da compra.
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[("pending", "Pendente"), ("paid", "Pago"), ("canceled", "Cancelado")],
    )

    def __str__(self):
        """
        Esta função define como o pedido aparece lá no painel do Django Admin.
        Em vez de aparecer 'Order object (1)', aparecerá 'Pedido #1 - Usuário: edwin'.
        """
        return f"Pedido #{self.id} - Usuário: {self.user.username}"
