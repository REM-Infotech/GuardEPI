from datetime import datetime
from typing import Optional

import pytz
from sqlalchemy.orm import Mapped

from app import db

epis_cautela = db.Table(
    "epis_cautela",
    db.Column(
        "produto_epi_id", db.Integer, db.ForeignKey("produto_epi.id"), primary_key=True
    ),
    db.Column(
        "registros_epi_id",
        db.Integer,
        db.ForeignKey("registros_epi.id"),
        primary_key=True,
    ),
)


class RegistrosEPI(db.Model):

    __tablename__ = "registros_epi"
    id = db.Column(db.Integer, primary_key=True)
    nome_epis: Mapped[Optional[list]] = db.relationship(
        "ProdutoEPI", secondary="epis_cautela", backref="registros_epi"
    )
    valor_total: float = db.Column(db.Float, nullable=False)
    funcionario: str = db.Column(db.String(length=64), nullable=False)
    data_solicitacao: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename: str = db.Column(db.Text, nullable=False)
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
