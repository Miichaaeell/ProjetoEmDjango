from django.test import TestCase
from boot.gerencia import enviar_resposta
# Create your tests here.


msg = 'show de bola'
tel = '5519999894514'
enviar_resposta(msg, tel)
