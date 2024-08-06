import pytz
from datetime import datetime

from app import db

class RegistrosEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nome_epis = db.Column(db.String(length=2048), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    funcionario = db.Column(db.String(length=64), nullable=False)
    data_solicitacao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    doc_cautela = db.Column(db.String(length=64), nullable=False)
    blob_cautela = db.Column(db.LargeBinary)
    
    def __init__(self, nome_epis: str, funcionario: str, data_solicitacao: datetime,
                 doc_cautela: str, valor_total: float) -> None:
        
        self.nome_epis = nome_epis
        self.funcionario = funcionario
        self.data_solicitacao = data_solicitacao
        self.doc_cautela = doc_cautela
        self.valor_total = valor_total