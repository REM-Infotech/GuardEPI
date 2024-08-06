import pytz
from datetime import datetime

from app import db

class EstoqueEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nome_epi: str, tipo_qtd: str, qtd_estoque: int):
        
        self.nome_epi = nome_epi
        self.tipo_qtd = tipo_qtd
        self.qtd_estoque = qtd_estoque

class EstoqueGrade(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    qtd_estoque = db.Column(db.Integer, nullable=False)
    
    def __init__(self, nome_epi: str, tipo_qtd: str, grade: str, qtd_estoque: int) -> None:
        self.nome_epi = nome_epi
        self.tipo_qtd = tipo_qtd
        self.grade = grade
        self.qtd_estoque = qtd_estoque

class RegistroEntradas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome_epi = db.Column(db.String(length=64), nullable=False)
    grade = db.Column(db.String(length=64), nullable=False)
    tipo_qtd = db.Column(db.String(length=64), nullable=False)
    qtd_entrada = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    
    def __init__(self, nome_epi: str, tipo_qtd: str, grade: str,
                 qtd_entrada: int, valor_total: float):
        
        self.nome_epi = nome_epi
        self.tipo_qtd = tipo_qtd
        self.qtd_entrada = qtd_entrada
        self.valor_total = valor_total
        self.grade = grade

class GradeEPI(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(length=32), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))
