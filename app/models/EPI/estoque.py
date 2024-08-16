import pytz
from datetime import datetime

from app import db

class EstoqueEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)

class EstoqueGrade(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)

class RegistroEntradas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_entrada = db.Column(db.Integer, nullable=False)
    data_entrada = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    valor_total = db.Column(db.Float, nullable=False)

class GradeEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(length=32), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))
