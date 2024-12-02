# Configuração do projeto

## Índice

- [Configuração do projeto](#configuração-do-projeto)
  - [Índice](#índice)
  - [Estrutura do projeto](#estrutura-do-projeto)
  - [Setup de ambiente:](#setup-de-ambiente)

## Estrutura do projeto

- [`APP`](./app/): É a pasta onde fica centralizado rotas, formulários e models do Flask

- [`Arquivo Config.`](./app/default_config.py): Arquivo de configuração do APP

_A partir de `/app`, teremos_:

- [`Models`](./app/models/): Onde ficam os models e bind's do SQL.

- [`Forms`](./app/Forms/): Formulários do projeto, sempre mantendo separados por funções.

- [`Routes`](./app/routes/): Rotas do projeto, sempre mantendo separados por funções.

## Setup de ambiente:

**Para linux**

- Verificar Versão do python instalado

  ```bash
  python3 --version
  # Retorna a versão python

  ```

- Caso a versão não corresponda

  - Adicione o [PPA DeadSnakes](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)

  > Disclaimer:
  > PPA do deadsnakes é apenas para o Ubuntu, verificar os manuais para sua distro caso nao corresponda

  ```bash
      sudo add-apt-repository ppa:deadsnakes/ppa
      sudo apt update
      sudo apt install python3.12
  ```

**Para Windows**

Recomenda-se baixar o instalador direto do site do [Python.org](https://python.org)

> Disclaimer:
> Use a versão correspondente ao informado no [Pyproject.toml](./pyproject.toml)

**Configuração Poetry**

_Usando [pipx](https://pipx.pypa.io/stable/installation/):_

```bash
# Windows (Reiniciar terminal após isso):
py -3.12 -m pip install --user pipx

# Ubuntu:
python3 -m pip install --user pipx

# Evitar configuração manual de variaveis de ambiente

pipx ensurepath --global

pipx install poetry


```

**Instalação do sistema**

```bash
# Dentro da pasta Raiz do projeto, execute:

poetry install

# Caso queira executar com os pacotes de Dev:

poetry install --with dev


```

**Patterns do .env**

```python
# .env

""" Porta do Projeto """
PORT = 5000

""" Configurações do servidor de E-mail """
MAIL_SERVER = smtp.exemplo.com
MAIL_PORT = 587
MAIL_USERNAME = 'mail@example.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = "mail@example.com"

""" URI do Redis """
REDIS_URI = "redis://localhost"


"""Criação de usuário ADM e uma empresa dummy"""
loginsys = "root"
nomeusr = "User Root"
emailusr = "root@example.com"

name_client="Empresa Model"
cpf_cnpj="12345678987654"

"""Configurações do banco de dados"""
LOGIN = "db_usr"
PASSWORD = "db_pass"
HOST = "localhost"
DATABASE = "database"


"""Variáveis para o Google Cloud Storage"""
project_id = "project_id"
bucket_name = "bucket_gcs"

""" Disclaimer: Chave entre aspas simples """
credentials_dict = '{}'


```
