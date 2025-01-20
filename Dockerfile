FROM python:3

# Atualizar pacotes e configurar locales
RUN apt-get update && apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    apt-get clean

ENV LANG=pt_BR.UTF-8
ENV LC_ALL=pt_BR.UTF-8

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Criar diretório de trabalho e copiar arquivos
COPY . /GuardEPI
WORKDIR /GuardEPI

# Instalar dependências
RUN poetry config virtualenvs.create false && poetry install --no-root

# Comando padrão
CMD ["poetry", "run", "python", "-m", "app"]
