from django.db import models
from django.conf import settings


class Feira(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    localidade = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11)
    data_criacao = models.DateField()

    def __str__(self):
        return self.nome


class Ingresso(models.Model):
    codigo = models.IntegerField()
    data_emissao = models.DateField()
    feira = models.ForeignKey(Feira, related_name='ingressos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, related_name='ingressos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ingresso {self.codigo} - {self.feira.nome}"


class Admin(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_criacao = models.DateField()

    def __str__(self):
        return self.usuario.username


class Expositor(models.Model):
    descricao = models.TextField()
    contato = models.CharField(max_length=100)  # Email ou telefone
    feiras = models.ManyToManyField(Feira, related_name='expositores')
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField()
    expositor = models.ForeignKey(Expositor, on_delete=models.CASCADE, related_name='produtos')
    data_criacao = models.DateField()

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    local = models.CharField(max_length=100)
    estado = models.CharField(max_length=30)
    cep = models.CharField(max_length=9)
    data_criacao = models.DateField()

    def __str__(self):
        return self.local


class Expoe(models.Model):
    expositor = models.ForeignKey(Expositor, related_name='feiras_expostas', on_delete=models.CASCADE)
    feira = models.ForeignKey(Feira, related_name='exposicoes', on_delete=models.CASCADE)
    data_criacao = models.DateField()

    def __str__(self):
        return f"{self.expositor} expõe na {self.feira}"
