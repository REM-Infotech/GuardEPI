from collections import Counter

from app import app
from app.models import (
    ClassesEPI,
    EstoqueGrade,
    Fornecedores,
    Funcionarios,
    GradeEPI,
    Marcas,
    ModelosEPI,
    ProdutoEPI,
)


def set_EpiCautelaChoices() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        database = EstoqueGrade.query.order_by(EstoqueGrade.nome_epi.asc()).all()
        epis = [epi.nome_epi for epi in database]
        count = Counter(epis)
        list_itens = [(item, item) for item in count]
        return list_itens


def set_ChoicesFuncionario() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [
            (epi.nome_funcionario, epi.nome_funcionario)
            for epi in Funcionarios.query.order_by(
                Funcionarios.nome_funcionario.asc()
            ).all()
        ]


def set_choices() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [
            (epi.nome_epi, epi.nome_epi)
            for epi in ProdutoEPI.query.order_by(ProdutoEPI.nome_epi.asc()).all()
        ]


def set_choicesGrade() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [(epi.grade, epi.grade) for epi in GradeEPI.query.all()]


def set_choicesFornecedor() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [(epi.fornecedor, epi.fornecedor) for epi in Fornecedores.query.all()]


def set_choicesMarca() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [(epi.marca, epi.marca) for epi in Marcas.query.all()]


def set_choicesModelo() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [(epi.modelo, epi.modelo) for epi in ModelosEPI.query.all()]


def set_choicesClasseEPI() -> list[tuple[str, str]]:  # pragma: no cover
    with app.app_context():
        return [(epi.classe, epi.classe) for epi in ClassesEPI.query.all()]
