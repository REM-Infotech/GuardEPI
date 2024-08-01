from app import db
from datetime import datetime
import pytz

class ProdutoEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ca = db.Column(db.String(length=64), nullable=False)
    cod_ca = db.Column(db.Integer)
    nome_epi = db.Column(db.String(length=64), nullable=False, unique=True)
    tipo_epi = db.Column(db.String(length=64), nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)
    qtd_entregar = db.Column(db.Integer, nullable=False)
    periodicidade_item = db.Column(db.Integer, nullable=False, default=10)
    data_ultima_troca = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    data_proxima_troca = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    fornecedor = db.Column(db.String(length=64))
    marca = db.Column(db.String(length=64))
    modelo = db.Column(db.String(length=64))
    imagem = db.Column(db.String(length=128))
    blob_imagem = db.Column(db.LargeBinary)

class GradeEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    ca = db.Column(db.String(length=64), nullable=False)
    cod_ca = db.Column(db.Integer)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_grade =  db.Column(db.String(length=64), nullable=False, default="Sem Categoria")
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)

class RegistrosEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    funcionario = db.Column(db.String(length=64), nullable=False)
    data_solicitacao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    doc_cautela = db.Column(db.String(length=64), nullable=False)
    blob_cautela = db.Column(db.LargeBinary)
    

