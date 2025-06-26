# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.utils import timezone
from .models import Feira, Expositor, Usuario, Ingresso # Adicionado Ingresso
from .forms import CadastroForm
from django.db.models import Q # Adicionado para o filtro
from django.contrib.auth.decorators import login_required # Adicionado para proteger views
from django.contrib import messages # Adicionado para feedback ao usuário

# ATUALIZADO: Adicionado filtro de busca
def pagina_inicial(request):
    busca = request.GET.get('busca', '')
    lista_de_feiras = Feira.objects.all().order_by('-data_inicio')

    if busca:
        lista_de_feiras = lista_de_feiras.filter(
            Q(nome__icontains=busca) | Q(localidade__icontains=busca)
        )

    context = {
        'feiras': lista_de_feiras,
        'busca': busca,  # Passa o termo de busca de volta para o template
    }
    
    return render(request, 'core/pagina_inicial.html', context)

# ATUALIZADO: Passa informações do ingresso para o template
def detalhes_feira(request, feira_id):
    feira = get_object_or_404(Feira, pk=feira_id)
    expositores_da_feira = feira.expositores.all()
    
    ingresso_usuario = None
    if request.user.is_authenticated:
        try:
            # Tenta encontrar o Usuario customizado correspondente ao User logado
            usuario_custom = Usuario.objects.get(nome=request.user.username)
            # Verifica se já existe um ingresso para este usuário e feira
            ingresso_usuario = Ingresso.objects.filter(feira=feira, usuario=usuario_custom).first()
        except Usuario.DoesNotExist:
            # Se não encontrar o Usuario customizado, não faz nada.
            # Isso pode acontecer se o 'admin' não tiver um 'Usuario' correspondente.
            pass

    context = {
        'feira': feira,
        'expositores': expositores_da_feira,
        'ingresso_usuario': ingresso_usuario, # Envia o ingresso (ou None) para o template
    }

    return render(request, 'core/detalhes_feira.html', context)

# ⚠️ PONTO DE ATENÇÃO: A lógica abaixo assume que o 'nome' no seu modelo 'Usuario'
# é o mesmo que o 'username' do 'User' do Django. Isso funciona com base na sua
# view de cadastro. Se isso mudar, essa lógica precisará ser ajustada.
# A melhor solução a longo prazo seria adicionar um OneToOneField entre User e Usuario.

# NOVO: View para emitir ingresso
@login_required
def emitir_ingresso(request, feira_id):
    if request.method == 'POST':
        feira = get_object_or_404(Feira, id=feira_id)
        try:
            usuario_custom = Usuario.objects.get(nome=request.user.username)
            
            # Verifica se o ingresso já não existe antes de criar
            if not Ingresso.objects.filter(feira=feira, usuario=usuario_custom).exists():
                Ingresso.objects.create(
                    feira=feira, 
                    usuario=usuario_custom,
                    data_emissao=timezone.now().date(),
                    # O campo 'codigo' precisa ser preenchido. Usaremos o ID do ingresso como um código simples.
                    # Uma solução melhor seria gerar um código aleatório.
                    codigo=0 # Será preenchido depois
                )
                messages.success(request, f"Ingresso para '{feira.nome}' emitido com sucesso!")
            else:
                messages.warning(request, "Você já possui um ingresso para esta feira.")

        except Usuario.DoesNotExist:
            messages.error(request, "Não foi possível emitir o ingresso. Perfil de usuário não encontrado.")
    
    return redirect('detalhes_feira', feira_id=feira_id)


# NOVO: View para excluir ingresso
@login_required
def excluir_ingresso(request, ingresso_id):
    if request.method == 'POST':
        try:
            usuario_custom = Usuario.objects.get(nome=request.user.username)
            ingresso = get_object_or_404(Ingresso, id=ingresso_id, usuario=usuario_custom)
            feira_id = ingresso.feira.id
            ingresso.delete()
            messages.info(request, "Seu ingresso foi cancelado.")
            return redirect('detalhes_feira', feira_id=feira_id)
        except Usuario.DoesNotExist:
            messages.error(request, "Não foi possível cancelar o ingresso. Perfil de usuário não encontrado.")
        except Ingresso.DoesNotExist:
            messages.error(request, "Ingresso não encontrado ou não pertence a você.")

    # Se a requisição não for POST ou der erro, redireciona para a página inicial
    return redirect('inicio')


def detalhes_expositor(request, expositor_id):
    expositor = get_object_or_404(Expositor, pk=expositor_id)
    lista_de_produtos = expositor.produtos.all()

    context = {
        'expositor': expositor,
        'produtos': lista_de_produtos
    }

    return render(request, 'core/detalhes_expositor.html', context)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            
            user = form.save()
            
            Usuario.objects.create(
                nome=username, # Alterado para usar username para garantir a ligação
                cpf=cpf,
                data_criacao=timezone.now().date()
            )
            
            login(request, user)
            return redirect('inicio')
    else:
        form = CadastroForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'core/cadastro.html', context)