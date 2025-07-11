from datetime import datetime

import pytz
from redis_om import HashModel
from sqlalchemy import Column, Integer, LargeBinary, String, Text

from app import db


class EPIsCautela(db.Model):
    __tablename__ = "epis_cautela"
    id = Column(Integer, primary_key=True)
    epis_saidas_id = Column(Integer, db.ForeignKey("registro_saidas.id"))
    epis_saidas = db.relationship("RegistroSaidas", backref="epis_cautela")

    registros_epi_id = Column(Integer, db.ForeignKey("registros_epi.id"))
    nome_epis = db.relationship("RegistrosEPI", backref="nome_epis_")
    cod_ref = Column(String(length=64), nullable=False)


class RegistrosEPI(db.Model):
    __tablename__ = "registros_epi"
    id = Column(Integer, primary_key=True)
    nome_epis = Column(String(length=2048))
    valor_total = Column(db.Float, nullable=False)
    funcionario = Column(String(length=64), nullable=False)
    data_solicitacao: datetime = Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename = Column(Text, nullable=False)
    blob_doc = Column(LargeBinary(length=(2**32) - 1))


class RegistrosEPIRedis(HashModel):
    id: int
    nome_epis: str
    valor_total: float
    funcionario: str
    data_solicitacao: datetime
    filename: str
    blob_doc: str
