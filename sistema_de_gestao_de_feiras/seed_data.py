import os
import django
from datetime import date, timedelta
import random
import traceback # Importe o traceback para debugar melhor

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_de_gestao_de_feiras.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Feira, Expositor, Produto, Organizador # Removi Organizador, supondo que não é mais um modelo separado

def run_seed():
    print("Iniciando o processo de seeding...")
    
    print("Limpando banco de dados...")
    User.objects.filter(is_superuser=False).delete()
    Feira.objects.all().delete()
    # Produto e Expositor são deletados em cascata quando o User é deletado, mas é bom garantir.
    Produto.objects.all().delete()
    Expositor.objects.all().delete()

    # --- INICIALIZAÇÃO DAS VARIÁVEIS PRINCIPAIS ---
    organizador_user = None
    expositores_criados = {} # Usaremos um dicionário para fácil acesso

    # --- CRIANDO ORGANIZADOR ---
    print("\nCriando organizador...")
    try:
        organizador_user = User.objects.create_user(username='organizador_eventos', password='password1234', first_name='Carlos Eventos', email='carlos@eventos.com')
        organizador = Organizador.objects.create(usuario=organizador_user, empresa='Eventos S.A.')
        # Se você usa Grupos, associe o organizador ao grupo aqui
        print("- Organizador 'organizador_eventos' criado.")
    except Exception:
        print("ERRO ao criar organizador:")
        traceback.print_exc()

    # --- CRIANDO EXPOSITORES ---
    print("\nCriando expositores e produtos...")
    try:
        # Expositor 1
        user1 = User.objects.create_user(username='techcorp', password='password1234', first_name='Ana Tech', email='ana@techcorp.com')
        exp1 = Expositor.objects.create(usuario=user1, descricao='Vendemos hardware de ponta.', contato='vendas@techcorp.com')
        Produto.objects.create(expositor=exp1, nome='Mouse Gamer RGB Pro', preco=250.00)
        expositores_criados['techcorp'] = exp1 # Adiciona ao dicionário
        print("- Expositor 'techcorp' criado.")

        # Expositor 2
        user2 = User.objects.create_user(username='gourmetfoods', password='password1234', first_name='Beto Gourmet', email='beto@gourmet.com')
        exp2 = Expositor.objects.create(usuario=user2, descricao='Comidas artesanais.', contato='contato@gourmet.com')
        Produto.objects.create(expositor=exp2, nome='Queijo Canastra Premiado', preco=85.50)
        expositores_criados['gourmetfoods'] = exp2
        print("- Expositor 'gourmetfoods' criado.")
        
        # Expositor 3
        user3 = User.objects.create_user(username='livraria_saber', password='password1234', first_name='Sara Livros', email='sara@saber.com')
        exp3 = Expositor.objects.create(usuario=user3, descricao='Livros raros e clássicos.', contato='livros@saber.com')
        Produto.objects.create(expositor=exp3, nome='Box Asimov', preco=180.00)
        expositores_criados['livraria_saber'] = exp3
        print("- Expositor 'livraria_saber' criado.")
    except Exception:
        print("ERRO ao criar expositores:")
        traceback.print_exc()

    # --- CRIANDO VISITANTES ---
    print("\nCriando visitantes...")
    # ... (código de visitantes continua o mesmo)
    try:
        User.objects.create_user(username='visitante_joao', password='password1234', first_name='João da Silva', email='joao@email.com')
        User.objects.create_user(username='visitante_maria', password='password1234', first_name='Maria Oliveira', email='maria@email.com')
        print("- Usuários visitantes 'visitante_joao' e 'visitante_maria' criados.")
    except Exception:
        print("ERRO ao criar visitantes:")
        traceback.print_exc()

    # --- CRIANDO FEIRAS E ASSOCIAÇÕES ---
    print("\nCriando Feiras e associando expositores...")
    # SÓ EXECUTA SE AS DEPENDÊNCIAS FORAM CRIADAS COM SUCESSO
    if organizador_user and expositores_criados:
        try:
            # DEFINIMOS A LISTA DE FEIRAS AQUI DENTRO, USANDO O DICIONÁRIO
            feiras_a_criar = [
                {'nome': 'Expo Tech 2025', 'localidade': 'São Paulo', 'aprovados': [expositores_criados['techcorp']], 'pendentes': [expositores_criados['gourmetfoods']]},
                {'nome': 'Bienal do Livro', 'localidade': 'Rio de Janeiro', 'aprovados': [expositores_criados['livraria_saber']]},
                {'nome': 'Festival Sabor & Arte', 'localidade': 'Belo Horizonte', 'aprovados': [expositores_criados['gourmetfoods']]},
                {'nome': 'Mega Game Convention', 'localidade': 'São Paulo', 'aprovados': [expositores_criados['techcorp']], 'pendentes': [expositores_criados['livraria_saber']]},
            ]
            
            start_date = date.today() + timedelta(days=10)
            for i, data in enumerate(feiras_a_criar):
                # Primeiro, cria o objeto Feira
                feira_obj = Feira.objects.create(
                    nome=data['nome'],
                    descricao=f"Descrição completa da {data['nome']}.",
                    localidade=data['localidade'],
                    data_inicio=start_date + timedelta(days=i*30),
                    data_fim=start_date + timedelta(days=i*30 + 4),
                    organizador=organizador
                )
                print(f"- Feira '{feira_obj.nome}' criada com ID {feira_obj.id}.")
                
                # Pega a lista de expositores a serem associados
                aprovados_a_associar = data.get('aprovados', [])
                if aprovados_a_associar:
                    print(f"  > Tentando associar {len(aprovados_a_associar)} expositor(es) aprovado(s): {[e.usuario.username for e in aprovados_a_associar]}")
                    feira_obj.expositores_aprovados.set(aprovados_a_associar)
                
                pendentes_a_associar = data.get('pendentes', [])
                if pendentes_a_associar:
                    print(f"  > Tentando associar {len(pendentes_a_associar)} expositor(es) pendente(s): {[e.usuario.username for e in pendentes_a_associar]}")
                    feira_obj.expositores_pendentes.set(pendentes_a_associar)

                # VERIFICAÇÃO IMEDIATA NO BANCO DE DADOS
                print(f"  > Verificação no DB: Aprovados na feira '{feira_obj.nome}': {list(feira_obj.expositores_aprovados.all())}\n")

        except Exception:
            print("ERRO DETALHADO ao criar feiras e associações:")
            traceback.print_exc()
    else:
        print("PULANDO CRIAÇÃO DE FEIRAS: Organizador ou Expositores não foram criados com sucesso.")

if __name__ == '__main__':
    run_seed()