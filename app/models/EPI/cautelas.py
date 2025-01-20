from datetime import datetime

import pytz

from app import db


class EPIsCautela(db.Model):

    __tablename__ = "epis_cautela"
    id = db.Column(db.Integer, primary_key=True)
    epis_saidas_id: int = db.Column(db.Integer, db.ForeignKey("registro_saidas.id"))
    epis_saidas = db.relationship("RegistroSaidas", backref="epis_cautela")

    registros_epi_id: int = db.Column(db.Integer, db.ForeignKey("registros_epi.id"))
    nome_epis = db.relationship("RegistrosEPI", backref="nome_epis_")
    cod_ref: str = db.Column(db.String(length=64), nullable=False)


class RegistrosEPI(db.Model):

    __tablename__ = "registros_epi"
    id = db.Column(db.Integer, primary_key=True)
    nome_epis: str = db.Column(db.String(length=2048))
    valor_total: float = db.Column(db.Float, nullable=False)
    funcionario: str = db.Column(db.String(length=64), nullable=False)
    data_solicitacao: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename: str = db.Column(db.Text, nullable=False)
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
