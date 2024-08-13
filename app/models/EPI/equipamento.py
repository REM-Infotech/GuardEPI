import pytz
from datetime import datetime

from app import db

class ProdutoEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ca = db.Column(db.String(length=64), nullable=False)
    cod_ca = db.Column(db.Integer)
    nome_epi = db.Column(db.String(length=64), nullable=False, unique=True)
    tipo_epi = db.Column(db.String(length=64), nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    qtd_entregar = db.Column(db.Integer, nullable=False)
    periodicidade_item = db.Column(db.Integer, nullable=False, default=10)
    vencimento = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    fornecedor = db.Column(db.String(length=64))
    marca = db.Column(db.String(length=64))
    modelo = db.Column(db.String(length=64))
    imagem = db.Column(db.String(length=128))
    blob_imagem = db.Column(db.LargeBinary)
    
    def __init__(self, ca: str, cod_ca: int, nome_epi: str, tipo_epi: str,
                 valor_unitario: float, qtd_entregar: int, periodicidade_item: int,
                 vencimento: datetime, fornecedor: str, marca: str, modelo: str) -> None:
        
        self.ca = ca
        self.cod_ca = cod_ca
        self.nome_epi = nome_epi
        self.tipo_epi = tipo_epi
        self.valor_unitario = valor_unitario
        self.qtd_entregar = qtd_entregar
        self.periodicidade_item = periodicidade_item
        self.vencimento = vencimento
        self.fornecedor = fornecedor
        self.marca = marca
        self.modelo = modelo
        