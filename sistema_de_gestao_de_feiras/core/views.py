from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .models import Feira, Expositor, Organizador, Ingresso, Produto
from .forms import CadastroForm, FeiraForm, ProdutoForm, ExpositorProfileForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm # Importe o novo form

def pagina_inicial(request):
    busca = request.GET.get('busca', '')
    feiras = Feira.objects.all().order_by('-data_inicio')
    if busca:
        feiras = feiras.filter(Q(nome__icontains=busca) | Q(localidade__icontains=busca))
    return render(request, 'core/pagina_inicial.html', {'feiras': feiras, 'busca': busca})

def detalhes_feira(request, feira_id):
    feira = get_object_or_404(Feira, pk=feira_id)
    ingresso_usuario = None
    if request.user.is_authenticated:
        ingresso_usuario = Ingresso.objects.filter(feira=feira, usuario=request.user).first()
    context = {
        'feira': feira,
        'expositores': feira.expositores_aprovados.all(),
        'ingresso_usuario': ingresso_usuario,
        'organizador': feira.organizador,
    }
    return render(request, 'core/detalhes_feira.html', context)

def detalhes_expositor(request, expositor_id):
    expositor = get_object_or_404(Expositor, pk=expositor_id)
    produtos = Produto.objects.filter(expositor=expositor)
    context = {
        'expositor': expositor,
        'produtos': produtos
    }
    return render(request, 'core/detalhes_expositor.html', context)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['welcome_message_sent'] = False
            return redirect('dashboard')
    else:
        form = CadastroForm()
    return render(request, 'core/cadastro.html', {'form': form})

@login_required
def dashboard(request):
    if hasattr(request.user, 'expositor') and not request.session.get('welcome_message_sent'):
        messages.success(request, f'Seja bem-vindo, Expositor {request.user.first_name or request.user.username}!')
        request.session['welcome_message_sent'] = True

    if hasattr(request.user, 'expositor'):
        meus_produtos = Produto.objects.filter(expositor=request.user.expositor)
        context = {'produtos': meus_produtos}
        return render(request, 'core/dashboard_expositor.html', context)
    elif hasattr(request.user, 'organizador'):
        feiras_organizadas = Feira.objects.filter(organizador=request.user.organizador).order_by('-data_inicio')
        context = {'feiras_organizadas': feiras_organizadas}
        return render(request, 'core/dashboard_organizador.html', context)
    else:
        meus_ingressos = Ingresso.objects.filter(usuario=request.user).order_by('-data_emissao')
        return render(request, 'core/dashboard_visitante.html', {'ingressos': meus_ingressos})

@login_required
def emitir_ingresso(request, feira_id):
    if request.method == 'POST':
        feira = get_object_or_404(Feira, id=feira_id)
        if not Ingresso.objects.filter(feira=feira, usuario=request.user).exists():
            Ingresso.objects.create(feira=feira, usuario=request.user)
            messages.success(request, f"Ingresso para '{feira.nome}' emitido com sucesso!")
        else:
            messages.warning(request, "Você já possui um ingresso para esta feira.")
    return redirect('detalhes_feira', feira_id=feira_id)

@login_required
def excluir_ingresso(request, ingresso_id):
    if request.method == 'POST':
        ingresso = get_object_or_404(Ingresso, id=ingresso_id, usuario=request.user)
        feira_id = ingresso.feira.id
        ingresso.delete()
        messages.info(request, "Seu ingresso foi cancelado.")
        return redirect('detalhes_feira', feira_id=feira_id)
    return redirect('inicio')

@login_required
def feira_criar(request):
    if not hasattr(request.user, 'organizador'):
        return redirect('dashboard')
    if request.method == 'POST':
        form = FeiraForm(request.POST)
        if form.is_valid():
            nova_feira = form.save(commit=False)
            nova_feira.organizador = request.user.organizador
            nova_feira.save()
            messages.success(request, f"A feira '{nova_feira.nome}' foi criada com sucesso!")
            return redirect('dashboard')
    else:
        form = FeiraForm()
    return render(request, 'core/feira_form.html', {'form': form, 'tipo': 'Criar'})

@login_required
def feira_editar(request, feira_id):
    feira = get_object_or_404(Feira, id=feira_id, organizador__usuario=request.user)
    if request.method == 'POST':
        form = FeiraForm(request.POST, instance=feira)
        if form.is_valid():
            form.save()
            messages.info(request, f"A feira '{feira.nome}' foi atualizada.")
            return redirect('dashboard')
    else:
        form = FeiraForm(instance=feira)
    return render(request, 'core/feira_form.html', {'form': form, 'tipo': 'Editar'})

@login_required
def feira_excluir(request, feira_id):
    feira = get_object_or_404(Feira, id=feira_id, organizador__usuario=request.user)
    if request.method == 'POST':
        nome_feira = feira.nome
        feira.delete()
        messages.warning(request, f"A feira '{nome_feira}' foi excluída.")
        return redirect('dashboard')
    return render(request, 'core/feira_confirm_delete.html', {'feira': feira})

@login_required
def produto_criar(request):
    if not hasattr(request.user, 'expositor'):
        return redirect('dashboard')
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            novo_produto = form.save(commit=False)
            novo_produto.expositor = request.user.expositor
            novo_produto.save()
            messages.success(request, f"Produto '{novo_produto.nome}' criado com sucesso!")
            return redirect('dashboard')
    else:
        form = ProdutoForm()
    return render(request, 'core/produto_form.html', {'form': form, 'tipo': 'Criar'})

@login_required
def produto_editar(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, expositor__usuario=request.user)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.info(request, f"Produto '{produto.nome}' atualizado.")
            return redirect('dashboard')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'core/produto_form.html', {'form': form, 'tipo': 'Editar'})

@login_required
def produto_excluir(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id, expositor__usuario=request.user)
    if request.method == 'POST':
        nome_produto = produto.nome
        produto.delete()
        messages.warning(request, f"Produto '{nome_produto}' foi excluído.")
        return redirect('dashboard')
    return render(request, 'core/produto_confirm_delete.html', {'produto': produto})

@login_required
def expositor_gerenciar_feiras(request):
    if not hasattr(request.user, 'expositor'):
        return redirect('dashboard')
    
    expositor = request.user.expositor
    
    if request.method == 'POST':
        feira_id = request.POST.get('feira_id')
        action = request.POST.get('action')
        feira = get_object_or_404(Feira, id=feira_id)
        if action == 'add':
            feira.expositores_pendentes.add(expositor)
            messages.success(request, f"Você agora está inscrito na feira '{feira.nome}'.")
        elif action == 'remove':
            # Verifica e remove da lista de aprovados, se ele estiver lá
            if expositor in feira.expositores_aprovados.all():
                feira.expositores_aprovados.remove(expositor)

            # Verifica e remove da lista de pendentes, se ele estiver lá
            if expositor in feira.expositores_pendentes.all():
                feira.expositores_pendentes.remove(expositor)

            messages.info(request, f"Você deixou de participar da feira '{feira.nome}'.")
        return redirect('expositor_gerenciar_feiras')

    feiras_aprovadas = Feira.objects.filter(expositores_aprovados=expositor)
    feiras_pendentes = Feira.objects.filter(expositores_pendentes=expositor)
    outras_feiras = Feira.objects.exclude(expositores_aprovados=expositor).exclude(expositores_pendentes=expositor)
    
    context = {
        'feiras_aprovadas': feiras_aprovadas,
        'feiras_pendentes': feiras_pendentes,
        'outras_feiras': outras_feiras,
    }
    return render(request, 'core/expositor_gerenciar_feiras.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        # Use o formulário personalizado
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('inicio')
    else:
        # Use o formulário personalizado
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'core/editar_perfil.html', {'form': form})

@login_required
def editar_perfil_expositor(request):
    expositor_profile = Expositor.objects.get(usuario=request.user)

    if request.method == 'POST':
        # Use o formulário personalizado aqui também
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ExpositorProfileForm(request.POST, instance=expositor_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil de expositor foi atualizado com sucesso!')
            return redirect('inicio')
    else:
        # E aqui
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ExpositorProfileForm(instance=expositor_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'core/editar_perfil_expositor.html', context)

@login_required
def gerenciar_expositores(request, feira_id):
    feira = get_object_or_404(Feira, pk=feira_id)
    # Garante que apenas o organizador da feira possa acessá-la
    if request.user != feira.organizador.usuario:
        return redirect('inicio') 

    pendentes = feira.expositores_pendentes.all()
    aprovados = feira.expositores_aprovados.all()

    context = {
        'feira': feira,
        'pendentes': pendentes,
        'aprovados': aprovados,
    }
    return render(request, 'core/gerenciar_expositores.html', context)

@login_required
def aprovar_expositor(request, feira_id, expositor_id):
    feira = get_object_or_404(Feira, pk=feira_id)
    expositor = get_object_or_404(Expositor, pk=expositor_id)
    # Verificação de segurança
    if request.user == feira.organizador.usuario:
        feira.expositores_aprovados.add(expositor)
        feira.expositores_pendentes.remove(expositor)
        messages.success(request, f'O expositor {expositor.usuario.get_full_name()} foi aprovado.')
    return redirect('gerenciar_expositores', feira_id=feira.id)

@login_required
def rejeitar_expositor(request, feira_id, expositor_id):
    feira = get_object_or_404(Feira, pk=feira_id)
    expositor = get_object_or_404(Expositor, pk=expositor_id)
    # Verificação de segurança
    if request.user == feira.organizador.usuario:
        feira.expositores_pendentes.remove(expositor)
        messages.success(request, f'A inscrição do expositor {expositor.usuario.get_full_name()} foi rejeitada.')
    return redirect('gerenciar_expositores', feira_id=feira.id)