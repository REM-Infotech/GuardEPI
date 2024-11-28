from datetime import datetime

import pytz

from app import db


class RegistrosEPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_epis = db.Column(db.String(length=2048), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    funcionario = db.Column(db.String(length=64), nullable=False)
    data_solicitacao = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    filename = db.Column(db.Text, nullable=False)
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
