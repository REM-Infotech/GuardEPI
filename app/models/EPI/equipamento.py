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
    fornecedor = db.Column(db.String(length=64))
    marca = db.Column(db.String(length=64))
    modelo = db.Column(db.String(length=64))
    filename = db.Column(db.String(length=128))
    blob_doc = db.Column(db.LargeBinary(length=(2**32) - 1))
    vencimento = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    descricao = db.Column(db.Text, default="Sem Descrição")

    def __init__(self, *args, **kwargs) -> None:
        super(ProdutoEPI, self).__init__(*args, **kwargs)


class Fornecedores(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    fornecedor = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))


class Marcas(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    marca = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))


class ModelosEPI(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    modelo = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))


class ClassesEPI(db.Model):

    id = db.Column(db.Integer, primary_key=True, unique=True)
    classe = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))


class GradeEPI(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.String(length=32), nullable=False, unique=True)
    descricao = db.Column(db.String(length=512))
