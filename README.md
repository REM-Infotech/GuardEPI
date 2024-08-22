# GuardEPI - Sistema de Gerenciamento do EPI
[![licence mit](https://img.shields.io/badge/licence-MIT-blue.svg)](./LICENSE)
[![Python 3.11](https://shields.io/badge/python-3.11%20-green?logo=python)](https://python.org/downloads/release/python-3119/)

## Requisitos para rodar o projeto

### Setup de ambiente:

- [`PPA DeadSnakes | Apenas Linux`](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
    > Verificar qual sua distro para o comando correto da instalação do PPA e instalação do python 3.11
    ### No ubuntu e debian (Normalmente utilizados para projetos):
    - `sudo add-apt-repository ppa:deadsnakes/ppa`
    - `sudo apt update`
    - `sudo apt install python3.11`

- [`Dependências do Projeto`](./requirements.txt), estarão em `requirements.txt`

## Como rodar na minha máquina?

#### Instalação do `venv (Virtual Environment)`

- `python3.11 -m venv .venv` 
ou
- `python3.11 -m venv .{nomepersonalizado}` 
    > Caso opte por usar um nome personalizado, adicionar o mesmo no `.gitignore` para a pasta não subir para o repositório

#### No Windows:
> Necessário habilitar execução de scripts `.ps1` da [Microsoft](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4)
- `.venv/Scripts/activate`
- `python -m pip install -r requirements.txt`

#### No Linux:

- `.venv/bin/activate`
- `python -m pip install -r requirements.txt`


#### Arquivo `.env`

> Crie um arquivo .env com esses parametros. Remova os comentários para evitar erros

``` Python

## .env

## Parâmetro necessário para executar o sistema no modo Debug
DEBUG = True

## Configurações do banco de dados
login = ""
password = ""
host = ""
database = ""

## Token Cloudflared. Ele será útil apenas em um sistema linux
## Pois ele fará a configuração automatica do tunnel Cloudflare.
## Útil para casos de Deploy em Production
CLOUDFLARED_TOKEN = "SEU_TOKEN_AQUI"


``` 


## Estrutura do projeto

- [`APP`](./app/): É a pasta onde fica centralizado rotas, formulários e models do Flask

- [`app.py`](./app/__init__.py): Arquivo de configuração do APP

#### A partir de `/app`, teremos:
- [`Models`](./app/models/): Onde ficam os models e bind's do SQL.

- [`Forms`](./app/Forms/): Formulários do projeto, sempre mantendo separados por funções.

- [`Routes`](./app/routes/): Formulários do projeto, sempre mantendo separados por funções.


