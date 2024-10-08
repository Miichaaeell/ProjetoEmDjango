from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('', views.inicio, name='inicio'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('painel', views.painel, name='painel'),
    path('listar_usuario', views.listar_usuario, name='listar_usuario'),
    path('alterar_senha', views.alterar_senha, name='alterar_senha'),
    path('editar_usuario/<int:id_user>', views.editar_usuario, name='editar_usuario'),
    path('detalhes_usuario/<int:id_user>', views.detalhes_usuario, name='detalhes_usuario'),
    path('excluir_usuario/<int:id_user>', views.excluir_usuario, name='excluir_usuario'),
    path('conversa/<int:id_cliente>', views.conversa, name='conversa'),
    path('chat', views.chat, name='chat'),

]