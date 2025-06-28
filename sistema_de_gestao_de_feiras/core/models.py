from django.db import models
from django.conf import settings

# --- PERFIS DE USUÁRIO ---
# Cada perfil está ligado a um único usuário padrão do Django.

class Organizador(models.Model):
    """ Representa um usuário que pode criar e gerenciar feiras. """
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100, blank=True, null=True, help_text="Nome da empresa organizadora, se aplicável.")

    def __str__(self):
        return self.usuario.username

class Expositor(models.Model):
    """ Representa um usuário que pode expor produtos em feiras. """
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descricao = models.TextField()
    contato = models.CharField(max_length=100)

    def __str__(self):
        return self.usuario.username

# --- MODELOS PRINCIPAIS ---

class Feira(models.Model):
    """ Representa um evento (feira). """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    localidade = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    organizador = models.ForeignKey(Organizador, on_delete=models.PROTECT, related_name='feiras_organizadas')
    expositores = models.ManyToManyField(Expositor, related_name='feiras_participantes', blank=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    """ Representa um item vendido por um Expositor. """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)
    expositor = models.ForeignKey(Expositor, on_delete=models.CASCADE, related_name='produtos')
    data_criacao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Ingresso(models.Model):
    """ Representa um ingresso de um Visitante para uma Feira. """
    data_emissao = models.DateTimeField(auto_now_add=True)
    feira = models.ForeignKey(Feira, related_name='ingressos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ingressos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ingresso de {self.usuario.username} para {self.feira.nome}"
    
# Este é um teste para forçar o salvamento    