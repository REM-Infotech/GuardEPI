from datetime import datetime
from typing import Type

import pytz
from sqlalchemy import LargeBinary

from app import db


class EstoqueEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi: str = db.Column(db.String(length=64), nullable=False)
    tipo_qtd: str = db.Column(db.String(length=64), nullable=False)
    qtd_estoque: int = db.Column(db.Integer, nullable=False)


class EstoqueGrade(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi: str = db.Column(db.String(length=64), nullable=False)
    grade: str = db.Column(db.String(length=64), nullable=False)
    tipo_qtd: str = db.Column(db.String(length=64), nullable=False)
    qtd_estoque: int = db.Column(db.Integer, nullable=False)


class RegistroEntradas(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi: str = db.Column(db.String(length=64), nullable=False)
    grade: str = db.Column(db.String(length=64), nullable=False)
    tipo_qtd: str = db.Column(db.String(length=64), nullable=False)
    qtd_entrada: int = db.Column(db.Integer, nullable=False)
    data_entrada: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    valor_total: float = db.Column(db.Float, nullable=False)
    justificativa: str = db.Column(db.String(length=512))

    filename: str = db.Column(db.String(length=128))
    blob_doc: LargeBinary = db.Column(db.LargeBinary(length=(2**32) - 1))


class RegistroSaidas(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi: str = db.Column(db.String(length=64), nullable=False)
    qtd_saida: int = db.Column(db.Integer, nullable=False)
    data_saida: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    valor_total: float = db.Column(db.Float, nullable=False)

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
