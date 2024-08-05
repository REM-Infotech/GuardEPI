import pytz
from datetime import datetime

from app import db

class EstoqueEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)
    
class RegistroEntradas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_entrada = db.Column(db.Integer, nullable=False)
    valor_unitario = db.Column(db.Float, nullable=False)

class GradeEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(length=6), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))
