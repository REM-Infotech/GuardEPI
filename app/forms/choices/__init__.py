from collections import Counter

from flask_sqlalchemy import SQLAlchemy
from quart import current_app as app

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


def set_EpiCautelaChoices() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        database = (
            db.session.query(EstoqueGrade)
            .filter(EstoqueGrade.qtd_estoque > 0)
            .order_by(EstoqueGrade.nome_epi.asc())
            .all()
        )

        database = filter(
            lambda x: (
                db.session.query(ProdutoEPI)
                .filter(ProdutoEPI.nome_epi == x.nome_epi)
                .first()
                is not None
            ),
            database,
        )

        epis = [epi.nome_epi for epi in database]
        count = Counter(epis)
        list_itens = [(item, item) for item in count]
        return list_itens


def set_ChoicesFuncionario() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [
            (epi.nome_funcionario, epi.nome_funcionario)
            for epi in db.session.query(Funcionarios)
            .order_by(Funcionarios.nome_funcionario.asc())
            .all()
        ]


def set_choices() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [
            (epi.nome_epi, epi.nome_epi)
            for epi in db.session.query(ProdutoEPI)
            .order_by(ProdutoEPI.nome_epi.asc())
            .all()
        ]


def set_choicesGrade() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [(epi.grade, epi.grade) for epi in db.session.query(GradeEPI).all()]


def set_choicesFornecedor() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [
            (epi.fornecedor, epi.fornecedor)
            for epi in db.session.query(Fornecedores).all()
        ]


def set_choicesMarca() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [(epi.marca, epi.marca) for epi in db.session.query(Marcas).all()]


def set_choicesModelo() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [(epi.modelo, epi.modelo) for epi in db.session.query(ModelosEPI).all()]


def set_choicesClasseEPI() -> list[tuple[str, str]]:
    with app.app_context():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        return [(epi.classe, epi.classe) for epi in db.session.query(ClassesEPI).all()]
