from django import forms
from django.contrib.auth.models import User
from .models import Expositor, Organizador, Feira, Produto
from django.db import transaction

# --- FORMULÁRIO DE CADASTRO DE USUÁRIOS ---
class CadastroForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
        ('visitante', 'Visitante (para participar das feiras)'),
        ('expositor', 'Expositor (para expor produtos)'),
        ('organizador', 'Organizador (para criar feiras)'),
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Eu quero me cadastrar como:",
        initial='visitante',
        required=True
    )
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, help_text="Mínimo de 12 caracteres.")
    password2 = forms.CharField(label="Confirmação da Senha", widget=forms.PasswordInput)
    descricao_expositor = forms.CharField(widget=forms.Textarea, required=False, label="Descrição do seu negócio")
    contato_expositor = forms.CharField(required=False, label="Contato profissional (email ou telefone)")
    empresa_organizador = forms.CharField(required=False, label="Nome da Empresa (opcional)")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        labels = {
            'first_name': 'Nome Completo',
            'username': 'Nome de Usuário',
            'email': 'E-mail',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if 'password' in cd and 'password2' in cd:
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('As senhas não correspondem.')
        return cd.get('password2')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        if user_type == 'expositor':
            if not cleaned_data.get('descricao_expositor'):
                self.add_error('descricao_expositor', 'Este campo é obrigatório para expositores.')
            if not cleaned_data.get('contato_expositor'):
                self.add_error('contato_expositor', 'Este campo é obrigatório para expositores.')
        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            user_type = self.cleaned_data.get('user_type')
            if user_type == 'expositor':
                Expositor.objects.create(
                    usuario=user,
                    descricao=self.cleaned_data.get('descricao_expositor'),
                    contato=self.cleaned_data.get('contato_expositor')
                )
            elif user_type == 'organizador':
                Organizador.objects.create(
                    usuario=user,
                    empresa=self.cleaned_data.get('empresa_organizador')
                )
        return user

# --- FORMULÁRIO PARA CRIAR/EDITAR FEIRAS (DO ORGANIZADOR) ---
class FeiraForm(forms.ModelForm):
    class Meta:
        model = Feira
        fields = ['nome', 'descricao', 'localidade', 'data_inicio', 'data_fim']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'data_fim': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'nome': 'Nome da Feira',
            'descricao': 'Descrição Completa',
            'localidade': 'Cidade/Estado',
            'data_inicio': 'Data de Início',
            'data_fim': 'Data de Fim',
        }

# --- FORMULÁRIO PARA PRODUTOS DO EXPOSITOR ---
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'quantidade']
        labels = {
            'nome': 'Nome do Produto',
            'descricao': 'Descrição do Produto',
            'preco': 'Preço (R$)',
            'quantidade': 'Quantidade em Estoque',
        }

# A CLASSE 'ExpositorFeirasForm' FOI REMOVIDA DAQUI, POIS ESTAVA INCORRETA.