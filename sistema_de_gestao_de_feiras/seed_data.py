# seed_data.py
import os
import django
from datetime import date, timedelta
import random

# Configure o ambiente do Django para que este script possa usar os modelos
# Altere 'sistema_de_gestao_de_feiras.settings' se o nome do seu projeto for diferente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_de_gestao_de_feiras.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Feira, Expositor, Produto

def run_seed():
    """
    Popula o banco de dados com dados de teste para desenvolvimento.
    Este script apaga os dados existentes (exceto superusuários) para evitar duplicatas.
    """
    print("Executando o script de seed para popular o banco de dados...")

    # Limpa dados antigos para começar do zero
    print("Limpando dados antigos...")
    Produto.objects.all().delete()
    Expositor.objects.all().delete()
    Feira.objects.all().delete()
    User.objects.filter(is_staff=False).delete() # Apaga usuários que não são da equipe/admin
    print("Dados antigos limpos com sucesso.")
    print("-" * 30)

    # 1. Criar usuários para serem os expositores
    print("Criando usuários expositores...")
    nomes_expositores = ['techcorp', 'gourmetfoods', 'livraria_saber', 'econoinvest', 'artesanatos_cia']
    expositores_criados = []
    for nome in nomes_expositores:
        user_django, created = User.objects.get_or_create(username=nome)
        if created:
            user_django.set_password('123')
            user_django.save()

        expositor, created = Expositor.objects.get_or_create(
            usuario=user_django,
            defaults={
                'descricao': f"Descrição do expositor {nome}.",
                'contato': f"contato@{nome}.com"
            }
        )
        expositores_criados.append(expositor)
        print(f"  - Expositor '{nome}' criado/verificado.")

    print("-" * 30)

    # 2. Dados das 20 Feiras
    feiras_data = [
        {'nome': 'Expo Tech 2025', 'localidade': 'São Paulo', 'cat': 'Tecnologia'},
        {'nome': 'Future Code Conference', 'localidade': 'Belo Horizonte', 'cat': 'Tecnologia'},
        {'nome': 'Feira de Inovação Digital', 'localidade': 'Curitiba', 'cat': 'Tecnologia'},
        {'nome': 'Startup Summit', 'localidade': 'Florianópolis', 'cat': 'Tecnologia'},
        {'nome': 'Gaming Experience', 'localidade': 'São Paulo', 'cat': 'Tecnologia'},
        {'nome': 'Bienal do Livro', 'localidade': 'Rio de Janeiro', 'cat': 'Leitura'},
        {'nome': 'Festa Literária de Paraty', 'localidade': 'Paraty', 'cat': 'Leitura'},
        {'nome': 'Salão do Livro de Porto Alegre', 'localidade': 'Porto Alegre', 'cat': 'Leitura'},
        {'nome': 'Feira de Quadrinhos e Mangás', 'localidade': 'São Paulo', 'cat': 'Leitura'},
        {'nome': 'Encontro de Poetas', 'localidade': 'Salvador', 'cat': 'Leitura'},
        {'nome': 'Festival Gastronômico de Tiradentes', 'localidade': 'Tiradentes', 'cat': 'Gastronomia'},
        {'nome': 'Sabor & Arte', 'localidade': 'Belo Horizonte', 'cat': 'Gastronomia'},
        {'nome': 'Feira de Vinhos e Queijos', 'localidade': 'Curitiba', 'cat': 'Gastronomia'},
        {'nome': 'Comida de Rua Fest', 'localidade': 'São Paulo', 'cat': 'Gastronomia'},
        {'nome': 'Festival do Chocolate', 'localidade': 'Gramado', 'cat': 'Gastronomia'},
        {'nome': 'Expo Investimentos', 'localidade': 'São Paulo', 'cat': 'Economia'},
        {'nome': 'Congresso de Finanças Pessoais', 'localidade': 'Brasília', 'cat': 'Economia'},
        {'nome': 'Feira do Empreendedor', 'localidade': 'Rio de Janeiro', 'cat': 'Economia'},
        {'nome': 'Fórum Econômico Nacional', 'localidade': 'Brasília', 'cat': 'Economia'},
        {'nome': 'Mercado de Ações Summit', 'localidade': 'São Paulo', 'cat': 'Economia'},
    ]

    # 3. Criar as feiras e associar expositores
    print("Criando feiras e associando expositores...")
    start_date = date.today()
    for i, data in enumerate(feiras_data):
        feira_obj = Feira.objects.create(nome=data['nome'], descricao=f"Descrição da {data['nome']}.", localidade=data['localidade'], data_inicio=start_date + timedelta(days=i*10), data_fim=start_date + timedelta(days=i*10 + 3))
        expositores_para_associar = random.sample(expositores_criados, k=random.randint(1, 3))
        feira_obj.expositores.set(expositores_para_associar)
        print(f"  - Feira '{feira_obj.nome}' criada em '{feira_obj.localidade}'.")
    
    print("-" * 30)

    # 4. Criar produtos para os expositores
    print("Criando produtos de exemplo...")
    for expositor in expositores_criados:
        for i in range(1, 3):
            Produto.objects.create(expositor=expositor, nome=f"Produto {i} de {expositor.usuario.username}", descricao="Um produto de alta qualidade.", preco=random.uniform(20.0, 200.0), quantidade=random.randint(10, 100), data_criacao=date.today())
    print("Produtos criados.")
    
    print("\n--- PROCESSO CONCLUÍDO! ---")
    print("Banco de dados populado com sucesso. Use 'python manage.py runserver' para iniciar o projeto.")

# Executa a função principal
if __name__ == '__main__':
    run_seed()