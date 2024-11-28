from datetime import datetime
from typing import Type

import pytz

from app import db


class EstoqueEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)


class EstoqueGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)


class RegistroEntradas(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_entrada = db.Column(db.Integer, nullable=False)
    data_entrada = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    valor_total = db.Column(db.Float, nullable=False)
    filename = db.Column(db.String(length=128))
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))


class RegistroSaidas(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    qtd_saida = db.Column(db.Integer, nullable=False)
    data_saida = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    valor_total = db.Column(db.Float, nullable=False)

    def __init__(
        self,
        nome_epi: str = None,
        qtd_saida: int = 1,
        data_saida: Type[datetime] = datetime.now(),
        valor_total: float = 0.00,
    ) -> None:
        self.nome_epi = nome_epi
        self.qtd_saida = qtd_saida
        self.data_saida = data_saida
        self.valor_total = valor_total
