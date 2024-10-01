from .gerencia import filtrar_dados, reply, enviar_resposta
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from os import environ
# Create your views here.
token = environ.get('TOKEN')
@csrf_exempt
def boot(request):
    if request.method == 'GET':
        key = request.GET['hub.challenge']
        verify_token = request.GET['hub.verify_token']
        if verify_token == token:
            return HttpResponse(key)
        else:
            return HttpResponse('Token incorreto')
    else:
        msg = json.loads(request.body)
        if 'contacts' in msg['entry'][0]['changes'][0]['value']:
            usuario = filtrar_dados(msg)
            res = reply(usuario[0], usuario[1], usuario[2])
            if res :
                status = enviar_resposta(res, usuario[0]['telefone'], 'boot')
                return HttpResponse(f'{status}')
            else:
                return HttpResponse('Atendimento')
        else:
            res = json.loads(request.body)
            print(f'Status message: {res["entry"][0]["changes"][0]["value"]["statuses"][0]["status"]}')
            return HttpResponse(f'Status message: {res["entry"][0]["changes"][0]["value"]["statuses"][0]["status"]}')
        

