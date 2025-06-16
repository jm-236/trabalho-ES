from django.db import models

# Create your models here.
# core/models.py

from django.db import models
from django.conf import settings # Usaremos para vincular ao usuário no futuro

class Feira(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    localidade = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    # Futuramente, podemos vincular a um organizador:
    # organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Expositor(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    contato = models.CharField(max_length=100) # Email ou telefone
    feiras = models.ManyToManyField(Feira, related_name='expositores') # Um expositor pode estar em várias feiras
    # Futuramente, podemos vincular a um usuário:
    # usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    expositor = models.ForeignKey(Expositor, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome
