# Formatar o código automaticamente com Black, isort e corrigir Ruff
format:
	@echo "Formatando o código com Black, isort e Ruff..."
	black .
	isort .
	ruff check . --fix

# Rodar apenas o pre-commit em todos os arquivos
pre-commit:
	@echo "Executando pre-commit em todos os arquivos..."
	pre-commit run --all-files

# Checar código com Flake8, Ruff e MyPy
lint:
	@echo "Verificando o código com Flake8, Ruff e MyPy..."
	flake8 .
	ruff check .
	mypy .

# Pipeline completo: formatar, checar e rodar pre-commit
check:
	@echo "Executando a pipeline completa..."
	make format
	make lint
	make pre-commit

# Instalar pre-commit no repositório
install-pre-commit:
	@echo "Instalando pre-commit no repositório..."
	pre-commit install
