
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario

class CadastroForm(UserCreationForm):
    nome = forms.CharField(max_length=100, label='Nome completo')
    cpf = forms.CharField(max_length=11, label='CPF')
    
    class Meta:
        model = User
        fields = ('username', 'nome', 'cpf', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação da senha'
