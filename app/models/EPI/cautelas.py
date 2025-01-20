from datetime import datetime

import pytz

from app import db


class epis_cautela(db.Model):

    __tablename__ = "epis_cautela"
    id = db.Column(db.Integer, primary_key=True)
    produto_epi_id: int = db.Column(db.Integer, db.ForeignKey("produto_epi.id"))
    registros_epi_id: int = db.Column(db.Integer, db.ForeignKey("registros_epi.id"))
    cod_ref: str = db.Column(db.String(length=64), nullable=False)


class RegistrosEPI(db.Model):

    __tablename__ = "registros_epi"
    id = db.Column(db.Integer, primary_key=True)
    # cod_saida =
    nome_epis = db.relationship("epis_cautela", backref="nome_epi_registros")
    valor_total: float = db.Column(db.Float, nullable=False)
    funcionario: str = db.Column(db.String(length=64), nullable=False)
    data_solicitacao: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename: str = db.Column(db.Text, nullable=False)
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
