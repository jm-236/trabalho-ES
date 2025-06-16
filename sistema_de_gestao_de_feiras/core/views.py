# core/views.py

from django.shortcuts import render, get_object_or_404
from .models import Feira, Expositor

def pagina_inicial(request):
    # 1. Busca os dados do banco
    lista_de_feiras = Feira.objects.all().order_by('-data_inicio')
    
    # 2. Cria o dicionário de contexto
    context = {
        'feiras': lista_de_feiras,
    }
    
    # 3. Retorna a renderização do template com o contexto
    return render(request, 'core/pagina_inicial.html', context)


def detalhes_feira(request, feira_id):
    # 1. Busca os dados do banco
    feira = get_object_or_404(Feira, pk=feira_id)
    expositores_da_feira = feira.expositores.all() 
    
    # 2. Cria o dicionário de contexto
    context = {
        'feira': feira,
        'expositores': expositores_da_feira,
    }

    # 3. Retorna a renderização do template com o contexto
    return render(request, 'core/detalhes_feira.html', context)

def detalhes_expositor(request, expositor_id):
    # 1. Busca o expositor específico pelo seu ID. Se não encontrar, retorna erro 404.
    expositor = get_object_or_404(Expositor, pk=expositor_id)
    
    # 2. Busca todos os produtos associados a este expositor.
    #    Isso funciona por causa do `related_name='produtos'` que definimos no model.
    lista_de_produtos = expositor.produtos.all()

    # 3. Monta o contexto para enviar ao template.
    context = {
        'expositor': expositor,
        'produtos': lista_de_produtos
    }

    return render(request, 'core/detalhes_expositor.html', context)
