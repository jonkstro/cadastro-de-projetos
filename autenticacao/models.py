from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Pessoa(models.Model):
    nome_completo = models.TextField()
    telefone = models.CharField(max_length=15)
    def __str__(self):
        return self.nome_completo