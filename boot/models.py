from django.db import models
from django.db.models.signals import post_save
from winotify import Notification, audio
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

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
    nome = models.CharField(max_length=72, blank=True)
    notificacao = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')

    def __str__(self):
        return str(self.mensagem)

    class Meta:
        db_table_comment = 'Mensagens recebias e enviadas para os clientes'
        ordering = ['date_created']
        verbose_name = 'Mensagens'

def Notificar(sender, instance, created, **kwargs):
    if instance.remetente == 'cliente' and instance.notificacao == True:
        notificacao = Notification(app_id="Projeto django", title=f"{instance.nome}", msg=instance, icon=r'C://Users/Michael Andrew/PycharmProjects/ProjetoEmDjango/main/static/imagens/favicon.ico')
        notificacao.set_audio(audio.LoopingAlarm10, loop=True)
        notificacao.add_actions(label='Responder', launch='http://127.0.0.1:8000/inicio')
        notificacao.show()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'Atendimento',
            {
                "type": "new_message",
                "message": instance.mensagem,
                "id": instance.cliente.id

            }
        )
        
        

post_save.connect(Notificar, sender=Mensagem)