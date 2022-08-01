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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=64)
    telefone = models.CharField(max_length=15)
    def __str__(self):
        return self.user.nome_completo