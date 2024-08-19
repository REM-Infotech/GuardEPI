from app import app
from app.models import ProdutoEPI, Funcionarios, GradeEPI, Fornecedores, Marcas, ModelosEPI, ClassesEPI

def set_ChoicesFuncionario() -> list[tuple[str, str]]:

    with app.app_context():
        return [(epi.nome_funcionario, epi.nome_funcionario) for epi in Funcionarios.query.all()]

def set_choices() -> list[tuple[str, str]]:

    with app.app_context():
        return [(epi.nome_epi, epi.nome_epi) for epi in ProdutoEPI.query.all()]

def set_choicesGrade() -> list[tuple[str, str]]:

    with app.app_context():
        return [(epi.grade, epi.grade) for epi in GradeEPI.query.all()]


def set_choicesFornecedor() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(epi.fornecedor, epi.fornecedor) for epi in Fornecedores.query.all()]

def set_choicesMarca() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(epi.marca, epi.marca) for epi in Marcas.query.all()]

def set_choicesModelo() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(epi.modelo, epi.modelo) for epi in ModelosEPI.query.all()]

def set_choicesClasseEPI() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(epi.classe, epi.classe) for epi in ClassesEPI.query.all()]