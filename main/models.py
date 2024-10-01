from django.db import models
# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=72)
    email = models.EmailField(max_length=254)
    usuario = models.CharField(max_length=72)
    senha = models.CharField(max_length=72)
    previlegio = models.CharField(max_length=72)
    date_created = models.DateField(auto_now_add=True, verbose_name='Data de Criação')
    last_login = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.nome
    
    class Meta:
        db_table_comment = "Usuarios do sistema"
        verbose_name  = 'Usuários'