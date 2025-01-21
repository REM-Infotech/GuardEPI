from datetime import datetime

import pytz

from app import db


class ProdutoEPI(db.Model):
    """
    ProdutoEPI represents a model for personal protective equipment (PPE) products.
    Attributes:
        id (int): Unique identifier for the PPE product.
        ca (str): Certificate of Approval (CA) number for the PPE product.
        cod_ca (int): Code associated with the CA number.
        nome_epi (str): Name of the PPE product.
        tipo_epi (str): Type/category of the PPE product.
        valor_unitario (float): Unit price of the PPE product.
        qtd_entregar (int): Quantity to be delivered.
        periodicidade_item (int): Periodicity of the item, default is 10.
        fornecedor (str): Supplier of the PPE product.
        marca (str): Brand of the PPE product.
        modelo (str): Model of the PPE product.
        filename (str): Filename associated with the PPE product.
        blob_doc (bytes): Binary large object (BLOB) document associated with the PPE product.
        vencimento (datetime): Expiration date of the PPE product, default is current datetime in GMT+4 timezone.
        descricao (str): Description of the PPE product, default is "Sem Descrição".
    Methods:
        __init__(*args: tuple, **kwargs: dict) -> None:
            Initializes a new instance of the ProdutoEPI class.
        __getattr__(self, attr: str):
            Retrieves the attribute specified by 'attr'. Raises an AttributeError if the attribute is not found.
    """

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


class Fornecedores(db.Model):
    """
    Fornecedores model represents suppliers in the database.
    Attributes:
        id (int): Unique identifier for the supplier.
        fornecedor (str): Name of the supplier, must be unique and not null.
        descricao (str): Description of the supplier.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    fornecedor: str = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao: str = db.Column(db.String(length=512))


class Marcas(db.Model):
    """
    Marcas model represents the brands of equipment in the database.
    Attributes:
        id (int): Unique identifier for the brand.
        marca (str): Name of the brand, must be unique and not null.
        descricao (str): Description of the brand, optional.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    marca: str = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao: str = db.Column(db.String(length=512))


class ModelosEPI(db.Model):
    """
    Model representing the EPI (Personal Protective Equipment) models.
    Attributes:
        id (int): The unique identifier for the EPI model.
        modelo (str): The name of the EPI model, must be unique and not null.
        descricao (str): A description of the EPI model.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    modelo: str = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao: str = db.Column(db.String(length=512))


class ClassesEPI(db.Model):
    """
    Represents a class of Personal Protective Equipment (PPE).
    Attributes:
        id (int): The unique identifier for the PPE class.
        classe (str): The name of the PPE class.
        descricao (str): A description of the PPE class.
    """

    id = db.Column(db.Integer, primary_key=True, unique=True)
    classe: str = db.Column(db.String(length=64), nullable=False, unique=True)
    descricao: str = db.Column(db.String(length=512))


class GradeEPI(db.Model):
    """
    Represents a GradeEPI model for the database.
    Attributes:
        id (int): The primary key for the GradeEPI.
        grade (str): The grade of the EPI, must be unique and not null.
        descricao (str): A description of the EPI grade.
    """

    id = db.Column(db.Integer, primary_key=True)
    grade: str = db.Column(db.String(length=32), nullable=False, unique=True)
    descricao: str = db.Column(db.String(length=512))
