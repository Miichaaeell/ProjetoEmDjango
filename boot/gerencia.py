from os import environ
from requests import request
from boot.respostas import *
from .models import Cliente, Mensagem

def filtrar_dados(dados):
    novo = False
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
        if cliente['msg'] == ['atendimento', 'atendente']:
            clientes.fluxo = 'atendimento'
            clientes.save()
        else:
            fluxo = clientes.fluxo
    # nova Query pois pode ter sido salvo um novo cliente
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


def reply(usuario, novo, fluxo):
    print(f'Cliente: {usuario["nome"]} \nMensagem: {usuario["msg"]}')
    print(f'Fluxo anterior: {fluxo}')
    if fluxo.lower() == 'atendimento' or 'atendimento' in usuario["msg"].lower() or 'atendente' in usuario["msg"].lower():
        atualizar_fluxo(usuario['telefone'], 'atendimento')
    elif fluxo.lower() == 'inicial' and usuario["msg"].lower() in ['bom dia', 'boa tarde', 'boa noite', 'ola', 'oi', 'tudo bem?']:
        return boas_vindas(usuario["nome"], novo)
    elif fluxo.lower() == 'inicial' and usuario['msg'].lower() in ['serviços', 'servico']:
        atualizar_fluxo(usuario['telefone'], 'Informações')
        return servicos(usuario['nome'])
    elif fluxo.lower() == 'informações' or usuario['msg'].lower() in ['orçamento' , 'orcamento']:
        atualizar_fluxo(usuario['telefone'], 'Cadastro E-mail')
        return cadastro_email(usuario['nome'])
    elif fluxo.lower() == 'cadastro e-mail':
        atualizar_fluxo(usuario['telefone'], 'Finalizando Orçamento')
        return orcamento(nome=usuario['nome'], email=usuario['msg'], telefone=usuario['telefone'])
    elif fluxo.lower() == 'finalizando orçamento':
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
