import os
import django
from datetime import date, timedelta
import random

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_de_gestao_de_feiras.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Feira, Expositor, Organizador, Produto

def run_seed():
    print("Iniciando o processo de seeding...")
    
    print("Limpando banco de dados de usuários não-admin e dados relacionados...")
    User.objects.filter(is_superuser=False).delete()
    # Os perfis, feiras, produtos, etc., serão deletados em cascata ou já foram.
    Feira.objects.all().delete()
    Produto.objects.all().delete()

    print("\nCriando usuários e perfis...")
    # --- ORGANIZADOR ---
    try:
        org_user = User.objects.create_user(username='organizador_eventos', password='password1234', first_name='Carlos Eventos', email='carlos@eventos.com')
        organizador = Organizador.objects.create(usuario=org_user, empresa='Eventos S.A.')
        print("- Organizador 'organizador_eventos' criado.")
    except Exception as e:
        print(f"Erro ao criar organizador: {e}")

    # --- EXPOSITORES ---
    expositores = []
    try:
        exp_user1 = User.objects.create_user(username='techcorp', password='password1234', first_name='Ana Tech', email='ana@techcorp.com')
        expositor1 = Expositor.objects.create(usuario=exp_user1, descricao='Vendemos hardware de ponta e gadgets inovadores.', contato='vendas@techcorp.com')
        Produto.objects.create(expositor=expositor1, nome='Mouse Gamer RGB Pro', preco=250.00, quantidade=50)
        expositores.append(expositor1)
        print("- Expositor 'techcorp' criado.")

        exp_user2 = User.objects.create_user(username='gourmetfoods', password='password1234', first_name='Beto Gourmet', email='beto@gourmet.com')
        expositor2 = Expositor.objects.create(usuario=exp_user2, descricao='Comidas artesanais, queijos e vinhos selecionados.', contato='contato@gourmet.com')
        Produto.objects.create(expositor=expositor2, nome='Queijo Canastra Premiado', preco=85.50, quantidade=30)
        expositores.append(expositor2)
        print("- Expositor 'gourmetfoods' criado.")
        
        exp_user3 = User.objects.create_user(username='livraria_saber', password='password1234', first_name='Sara Livros', email='sara@saber.com')
        expositor3 = Expositor.objects.create(usuario=exp_user3, descricao='Livros raros, clássicos da literatura e edições de colecionador.', contato='livros@saber.com')
        Produto.objects.create(expositor=expositor3, nome='Box Asimov - Trilogia da Fundação', preco=180.00, quantidade=15)
        expositores.append(expositor3)
        print("- Expositor 'livraria_saber' criado.")
    except Exception as e:
        print(f"Erro ao criar expositores: {e}")

    # --- VISITANTES ---
    try:
        User.objects.create_user(username='visitante_joao', password='password1234', first_name='João da Silva', email='joao@email.com')
        User.objects.create_user(username='visitante_maria', password='password1234', first_name='Maria Oliveira', email='maria@email.com')
        print("- Usuários visitantes 'visitante_joao' e 'visitante_maria' criados.")
    except Exception as e:
        print(f"Erro ao criar visitantes: {e}")

    print("\nCriando Feiras...")
    try:
        feiras_data = [
            {'nome': 'Expo Tech 2025', 'localidade': 'São Paulo', 'expositores': [expositor1]},
            {'nome': 'Bienal do Livro', 'localidade': 'Rio de Janeiro', 'expositores': [expositor3]},
            {'nome': 'Festival Sabor & Arte', 'localidade': 'Belo Horizonte', 'expositores': [expositor2]},
            {'nome': 'Mega Game Convention', 'localidade': 'São Paulo', 'expositores': [expositor1]},
            {'nome': 'Feira Literária de Ouro Preto', 'localidade': 'Ouro Preto', 'expositores': [expositor3]},
        ]
        start_date = date.today() + timedelta(days=10)
        for i, data in enumerate(feiras_data):
            feira_obj = Feira.objects.create(
                nome=data['nome'],
                descricao=f"Descrição completa e detalhada da {data['nome']}.",
                localidade=data['localidade'],
                data_inicio=start_date + timedelta(days=i*30),
                data_fim=start_date + timedelta(days=i*30 + 4),
                organizador=organizador
            )
            feira_obj.expositores.set(data['expositores'])
            print(f"- Feira '{feira_obj.nome}' criada e associada a expositores.")
    except Exception as e:
        print(f"Erro ao criar feiras: {e}")
        
    print("\n--- PROCESSO CONCLUÍDO! ---")
    print("Execute 'python manage.py runserver' para iniciar o servidor.")

if __name__ == '__main__':
    run_seed()