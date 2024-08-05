import pytz
from datetime import datetime

from app import db

class RegistrosEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    funcionario = db.Column(db.String(length=64), nullable=False)
    data_solicitacao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    doc_cautela = db.Column(db.String(length=64), nullable=False)
    blob_cautela = db.Column(db.LargeBinary)