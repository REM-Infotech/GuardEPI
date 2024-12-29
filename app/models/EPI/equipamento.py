from datetime import datetime

import pytz

from app import db


class ProdutoEPI(db.Model):

    __tablename__ = "produto_epi"
    id: int = db.Column(db.Integer, primary_key=True, unique=True)
    ca: str = db.Column(db.String(length=64), nullable=False)
    cod_ca: int = db.Column(db.Integer)
    nome_epi: str = db.Column(db.String(length=64), nullable=False, unique=True)
    tipo_epi: str = db.Column(db.String(length=64), nullable=False)
    valor_unitario: float = db.Column(db.Float, nullable=False)
    qtd_entregar: int = db.Column(db.Integer, nullable=False)
    periodicidade_item: int = db.Column(db.Integer, nullable=False, default=10)
    fornecedor: str = db.Column(db.String(length=64))
    marca: str = db.Column(db.String(length=64))
    modelo: str = db.Column(db.String(length=64))
    filename: str = db.Column(db.String(length=128))
    blob_doc: bytes = db.Column(db.LargeBinary(length=(2**32) - 1))
    vencimento: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    descricao: str = db.Column(db.Text, default="Sem Descrição")

    def __init__(self, *args: tuple, **kwargs: dict) -> None:  # pragma: no cover
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr: str):  # pragma: no cover

        func = super().__getattr__(attr)
        if not func:
            func = getattr(self, attr)
            if not func:
                raise AttributeError(f"Attribute {attr} not found")

        return func


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
