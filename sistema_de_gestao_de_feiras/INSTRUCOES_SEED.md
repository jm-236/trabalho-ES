# Como Popular o Banco de Dados para Desenvolvimento

Este projeto usa um script (`seed_data.py`) para criar um banco de dados de teste com 20 feiras, 5 expositores e seus produtos. Isso garante que todos na equipe tenham os mesmos dados para trabalhar, evitando conflitos com o arquivo `db.sqlite3`.

Siga estes passos sempre que precisar criar ou recriar um banco de dados de teste limpo.

### Pré-requisitos

1.  Baixe as últimas atualizações do projeto com o comando:
    ```dentro do terminal:

    git pull origin main

    ```
2.  Certifique-se de que seu ambiente virtual Python está ativado.

### Passos para Executar o Seed

1.  **Apague seu banco de dados local (se ele existir).**
    Para garantir que você comece do zero, apague o arquivo `db.sqlite3` da pasta do projeto.

2.  **Navegue até a pasta correta.**
    Abra seu terminal e certifique-se de que você está na pasta raiz do projeto (a mesma que contém o arquivo `manage.py`).

3.  **Execute o script de seed.**
    No terminal, rode o seguinte comando:
    ```dentro do terminal:

    python seed_data.py
    ```

4.  **Verifique o resultado.**
    O script levará alguns segundos para rodar e exibirá mensagens de "criado com sucesso".

5.  **Inicie o servidor.**
    Agora você está pronto para rodar o projeto com os dados de teste!
    ```dentro do terminal:

    python manage.py runserver
    ```

Pronto! Seu ambiente de desenvolvimento está populado e pronto para usar.