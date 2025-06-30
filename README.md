# Sistema de Divulgação e Gestão de Feiras

Este é o repositório do projeto final da disciplina de Engenharia de Software, um sistema web completo desenvolvido em Django para a divulgação e gerenciamento de feiras e eventos.

A plataforma permite que diferentes tipos de usuários (Visitantes, Expositores e Organizadores) interajam com o sistema, cada um com suas próprias permissões e funcionalidades, desde a emissão de ingressos até o gerenciamento completo de eventos e produtos.

## Estrutura de Diretórios do Repositório

Este repositório está organizado da seguinte forma para facilitar a navegação e a avaliação do projeto:

### 📁 `docs/`

Este diretório contém toda a documentação gerada durante o ciclo de vida do projeto. Inclui a especificação de requisitos funcionais e não funcionais, a descrição da arquitetura do software, a descrição da infraestrutura de produção e os storyboards com wireframes da interface de usuário.

### 📁 `kanban/`

Aqui estão armazenados os registros visuais (`screenshots`) do quadro Kanban utilizado para o gerenciamento ágil do projeto. Os prints representam o estado do quadro em diferentes momentos, demonstrando a evolução das tarefas desde o "Backlog" até a "Conclusão".

### 📁 `sistema_gestao_de_feiras/`

Esta é a pasta principal que contém todo o código-fonte da aplicação Django. O projeto foi desenvolvido seguindo o padrão de arquitetura MVT (Model-View-Template) para garantir a modularidade e manutenibilidade do código.

#### Como Rodar o Projeto Localmente

Para executar o sistema em um ambiente de desenvolvimento local, siga os passos abaixo.

**Pré-requisitos:**

  * Python 3.10 ou superior
  * `pip` (gerenciador de pacotes do Python)

**1. Clone o Repositório**

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd sistema_gestao_de_feiras
```

**2. Crie e Ative um Ambiente Virtual**
É uma boa prática isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no macOS/Linux
source venv/bin/activate
```

**3. Instale as Dependências**
O projeto depende do Django e outras bibliotecas. Crie o arquivo `requirements.txt` se ainda não tiver um, e depois instale-o.

```bash
# Se não tiver o arquivo, gere-o com o ambiente ativado:
pip freeze > requirements.txt

# Instale as dependências listadas no arquivo
pip install -r requirements.txt
```

**4. Aplique as Migrações do Banco de Dados**
Este comando irá criar o banco de dados SQLite (`db.sqlite3`) e aplicar a estrutura dos modelos.

```bash
python manage.py migrate
```

**5. Crie um Superusuário**
Você precisará de um superusuário para acessar o painel de administração (`/admin`).

```bash
python manage.py createsuperuser
```

Siga as instruções para definir nome de usuário, email e senha.

**6. (Opcional) Popule o Banco de Dados com Dados de Teste**
Para testar a aplicação com dados pré-cadastrados (usuários, feiras, produtos), execute o script de seeding.

```bash
python seed_data.py
```

**7. Inicie o Servidor de Desenvolvimento**

```bash
python manage.py runserver
```

A aplicação estará rodando em `http://127.0.0.1:8000/`. Você já pode acessar no seu navegador.

### 📁 `video/`

Esta pasta contém um arquivo de texto com o link para o vídeo de demonstração do protótipo funcional. O vídeo apresenta as principais jornadas dos usuários (Visitante, Expositor e Organizador), testando e validando as funcionalidades implementadas conforme os requisitos do projeto.
