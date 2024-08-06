from app import db
from datetime import datetime
import pytz
class Funcionarios(db.Model):
    
    __tablename__ = 'funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(length=6), nullable=False, unique=True)
    nome_funcionario = db.Column(db.String(length=64), nullable=False)
    cpf_funcionario = db.Column(db.String(length=14), nullable=False, unique=True)
    email_funcionario = db.Column(db.String(length=64))
    deficiencia = db.Column(db.String(length=64))
    data_admissao = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Etc/GMT+4')))
    cargo = db.Column(db.String(length=64))
    departamento = db.Column(db.String(length=64))
    empresa = db.Column(db.String(length=64))

class Cargos(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(length=6), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))
    
class Departamento(db.Model):
    
    __tablename__ = "departamentos"
    id = db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(length=6), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))

class Empresa(db.Model):
    
    __tablename__ = 'empresa'
    id = db.Column(db.Integer, primary_key=True)
    nome_empresa = db.Column(db.String(length=64))
    cnpj_empresa = db.Column(db.String(length=64))
    imagem = db.Column(db.String(length=128))
    blob_imagem = db.Column(db.LargeBinary)
