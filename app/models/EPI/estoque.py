from datetime import datetime
from typing import Type

import pytz
from sqlalchemy import Column, DateTime, Float, Integer, LargeBinary, String

from app import db


class EstoqueEPI(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    nome_epi = Column(String(length=64), nullable=False)
    tipo_qtd = Column(String(length=64), nullable=False)
    qtd_estoque = Column(Integer, nullable=False)


class EstoqueGrade(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    nome_epi = Column(String(length=64), nullable=False)
    grade = Column(String(length=64), nullable=False)
    tipo_qtd = Column(String(length=64), nullable=False)
    qtd_estoque = Column(Integer, nullable=False)


class RegistroEntradas(db.Model):
    id = Column(Integer, primary_key=True, unique=True)
    nome_epi = Column(String(length=64), nullable=False)
    grade = Column(String(length=64), nullable=False)
    tipo_qtd = Column(String(length=64), nullable=False)
    qtd_entrada = Column(Integer, nullable=False)
    data_entrada = Column(DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4")))
    valor_total = Column(Float, nullable=False)
    justificativa = Column(String(length=512))

    filename = Column(String(length=128))
    blob_doc = Column(LargeBinary(length=(2**32) - 1))


class RegistroSaidas(db.Model):
    __tablename__ = "registro_saidas"
    id = Column(Integer, primary_key=True, unique=True)
    nome_epi = Column(String(length=64), nullable=False)
    qtd_saida = Column(Integer, nullable=False)
    data_saida = Column(DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4")))
    valor_total = Column(Float, nullable=False)

    def __init__(
        self,
        nome_epi=None,
        qtd_saida=1,
        data_saida: Type[datetime] = datetime.now(),
        valor_total: float = 0.00,
    ) -> None:
        self.nome_epi = nome_epi
        self.qtd_saida = qtd_saida
        self.data_saida = data_saida
        self.valor_total = valor_total
