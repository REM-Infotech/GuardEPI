from datetime import datetime

import pytz

from app import db


class epis_cautela(db.Model):

    __tablename__ = "epis_cautela"
    id = db.Column(db.Integer, primary_key=True)
    produtos_epi_id: int = db.Column(db.Integer, db.ForeignKey("produto_epi.id"))
    produtos_epi = db.relationship("ProdutoEPI", backref="epis_cautela_")

    registros_epi_id: int = db.Column(db.Integer, db.ForeignKey("registros_epi.id"))
    nome_epis = db.relationship("RegistrosEPI", backref="epis_cautela_")


class RegistrosEPI(db.Model):

    __tablename__ = "registros_epi"
    id = db.Column(db.Integer, primary_key=True)
    cod_ref: str = db.Column(db.String(length=64), nullable=False)
    valor_total: float = db.Column(db.Float, nullable=False)
    funcionario: str = db.Column(db.String(length=64), nullable=False)
    data_solicitacao: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename: str = db.Column(db.Text, nullable=False)
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
