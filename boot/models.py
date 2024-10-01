from django.db import models
# Create your models here.

class Cliente(models.Model):
    nome = models.CharField(max_length=72)
    telefone = models.CharField(max_length=72)
    email = models.CharField(max_length=128, default='Cadastrar')
    fluxo = models.CharField(max_length=72, default='Inicial')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')



    def __str__(self):
        return self.nome

    class Meta:
        db_table_comment = 'Clientes que entraram em contato via whatsapp'
        ordering = ['nome']
        verbose_name = 'Clientes'

class Mensagem(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mensagem = models.TextField()
    remetente = models.CharField('cliente', max_length=72)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')

    def __str__(self):
        return str(self.mensagem)

    class Meta:
        db_table_comment = 'Mensagens recebias e enviadas para os clientes'
        ordering = ['date_created']
        verbose_name = 'Mensagens'

