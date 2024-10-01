from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from boot.gerencia import enviar_resposta
from boot.models import Cliente
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            messages.success(request, "loggin Succes!")
            login(request, user)
            return redirect('inicio')

    return render(request, 'login.html')

@login_required(login_url='login')
def logout_user(request):
     logout(request)
     return redirect('login')

@login_required(login_url='login')
def inicio(request):
    mensagens = []
    users = Cliente.objects.all()
    for usuario in users:
        dict = {}
        dict['id'] = usuario.id
        dict["nome"] = usuario.nome
        dict['fluxo'] = usuario.fluxo
        todas_mensagens = usuario.mensagem_set.all()
        list_mensagens = []
        for msg in todas_mensagens:
            list_mensagens.append(msg.mensagem)
        dict['mensagem'] = list_mensagens
        dict['ultima_mensagem'] = list_mensagens[-1][:20]
        mensagens.append(dict)   
    return render(request, 'inicio.html',  {'clientes': mensagens} )

@login_required(login_url='login')   
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        previlegio = request.POST['previlegio']
        users_exist = User.objects.get(username=username)
        if users_exist:
            return render(request, 'cadastro.html', {'erro': 'Usuário já cadastrado'})
        else:
            user = User.objects.create_user(username, email, password)
            user.first_name = nome
            if previlegio == 'Administrador':
                user.is_staff = True
            user.save()
            return redirect('inicio')
    else:
        return render(request, 'cadastro.html')

@login_required(login_url='login')
def listar_usuario(request):
    users = User.objects.all()
    if request.method == 'GET':
        return render(request, 'listar_usuarios.html', {'usuarios': users})
    else:
        nome = request.POST['nome']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        previlegio = request.POST['previlegio']
        user = User.objects.get(username=username)
        user.first_name = nome
        user.username = username
        user.email = email
        user.set_password(password)
        if previlegio == 'Administrador':
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()
        return render(request, 'listar_usuarios.html', {'usuarios': users})

@login_required(login_url='login')
def painel(request):
    return render(request, 'painel.html')

@login_required(login_url='login')
def alterar_senha(request):
    if request.method == 'POST':
        user = request.user
        user_change = User.objects.get(id=user.id)
        password = request.POST['senha']
        user_change.set_password(password)
        user_change.save()
        logout(request)
        return redirect('login')
    else:
        return render(request, 'alterar_senha.html')

@login_required(login_url='login')
def editar_usuario(request, id_user):
    user = User.objects.get(id=id_user)
    return render(request, 'editar_usuario.html', {'usuario': user})

@login_required(login_url='login')
def detalhes_usuario(request, id_user):
    user = User.objects.get(id=id_user)
    return render(request, 'detalhes_usuario.html', {'usuario': user})

@login_required(login_url='login')
def excluir_usuario(request, id_user):
    user = User.objects.get(id=id_user)
    user.delete()
    return redirect('listar_usuario')

@xframe_options_exempt
def conversa(request, id_cliente):
    cliente = Cliente.objects.filter(id=id_cliente).first()
    if request.method == 'POST':
        msg = request.POST['mensagem']
        enviar_resposta(msg=msg, telefone=cliente.telefone, remetente=request.user)
    mensagens = cliente.mensagem_set.all()
    return render(request, 'conversa.html', {'cliente':cliente, 'mensagens':mensagens})
   

