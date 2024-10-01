from os import environ
from requests import request
from boot.respostas import *
from .models import Cliente, Mensagem
#from atendimento.atendimento import atendente
def filtrar_dados(dados):
    novo = False
    fluxo = ''
    cliente = {}
    cliente['nome'] = dados['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
    cliente['telefone'] = dados['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
    cliente['msg'] = dados['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    clientes = Cliente.objects.filter(telefone=cliente['telefone']).first()
    if not clientes:
        new_cliente = Cliente(nome=cliente['nome'], telefone=cliente['telefone'])
        new_cliente.save()
        novo = True
        fluxo = 'inicial'
    else:
        fluxo = clientes.fluxo
    user = Cliente.objects.filter(telefone=cliente['telefone']).first()
    if user.fluxo == 'atendimento':
        msg = Mensagem(cliente=user, mensagem=cliente['msg'], remetente='cliente', nome=user.nome, notificacao=True)
    else:
        msg = Mensagem(cliente=user, mensagem=cliente['msg'], remetente='cliente', nome=user.nome)
    msg.save()
    return cliente, novo, fluxo

def atualizar_fluxo(telefone, fluxo):
    cliente = Cliente.objects.filter(telefone=telefone).first()
    cliente.fluxo = fluxo
    cliente.save()

def atendente(nome, telefone, msg):
    print(f'Nome: {nome} \nTelefone: {telefone}\nMensagem: {msg}')

def reply(usuario, novo, fluxo):
    print(f'Cliente: {usuario["nome"]} \nMensagem: {usuario["msg"]}')
    print(f'Fluxo anterior: {fluxo}')
    if fluxo == 'atendimento' or 'atendimento' in usuario["msg"] or 'atendente' in usuario["msg"]:
        atualizar_fluxo(usuario['telefone'], 'atendimento')
    elif fluxo == 'inicial' and usuario["msg"] in 'bom dia, boa tarde, boa noite, ola, oi, dia, noite, tarde, bom, boa, tudo bem':
        return boas_vindas(usuario["nome"], novo)
    elif fluxo == 'inicial' and usuario['msg'] in 'serviços servico':
        atualizar_fluxo(usuario['telefone'], 'Informações')
        return servicos(usuario['nome'])
    elif fluxo == 'Informações' or usuario['msg'] in 'orçamento , orcamento':
        atualizar_fluxo(usuario['telefone'], 'Cadastro E-mail')
        return cadastro_email(usuario['nome'])
    elif fluxo == 'Cadastro E-mail':
        atualizar_fluxo(usuario['telefone'], 'Finalizando Orçamento')
        return orcamento(nome=usuario['nome'], email=usuario['msg'], telefone=usuario['telefone'])
    elif fluxo == 'Finalizando Orçamento':
        atualizar_fluxo(usuario['telefone'], 'inicial')
        return despedida(usuario['nome'], usuario['telefone'], usuario['msg'])
    else:
        return 'Desculpe, mas faltou alguma informação, poderia me enviar os dados novamente, lembrando que todas as informações são essências para nosso atendimento'

def enviar_resposta(msg, telefone, remetente):
    user = Cliente.objects.filter(telefone=telefone).first()
    message_save = Mensagem(cliente=user, mensagem=msg, remetente=remetente)
    message_save.save()
    bearer = environ.get('BEARER_TOKEN')
    data = {'messaging_product': 'whatsapp',
            'to': telefone,
            'type': 'text',
            'text': {'body': f'{msg}'}}
    r = request(method='POST',
                         url='https://graph.facebook.com/v20.0/254050617801879/messages',
                         headers={'Authorization': f'Bearer {bearer}'},
                         json=data)
    print(r)
    return str(r)
