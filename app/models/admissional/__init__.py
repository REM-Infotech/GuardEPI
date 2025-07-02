# noqa: D104
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)

from app import db

files = db.Table(
    "files",
    Column("file_id", Integer, ForeignKey("file.id"), primary_key=True),
    Column(
        "form_admissional_id",
        Integer,
        ForeignKey("form_admissional.id"),
        primary_key=True,
    ),
)


class FormAdmissional(db.Model):  # noqa: D101
    __tablename__ = "form_admissional"
    id = Column(Integer, primary_key=True)
    submited = Column(Boolean, nullable=False, default=False)
    nome = Column(String(length=128))
    cpf = Column(String(length=128))
    email = Column(String(length=128))
    data_nascimento = Column(String(length=128))
    telefone = Column(String(length=128))
    endereco = Column(String(length=128))
    complemento = Column(String(length=128))
    cidade = Column(String(length=128))
    cep = Column(String(length=128))
    estado = Column(String(length=128))
    genero = Column(String(length=128))
    corRaca = Column(String(length=128))  # noqa: N815
    grauEscolaridade = Column(String(length=128))  # noqa: N815
    estadoCivil = Column(String(length=128))  # noqa: N815
    numero_residencia = Column(String(length=128))

    form_registry_id = Column(Integer, ForeignKey("registry_admissao.id"))
    form_registry = db.relationship("RegistryAdmissao", backref="form_registry")

    files = db.relationship(
        "FileModel",
        secondary="files",
        backref=db.backref("form", lazy=True),
    )


class RegistryAdmissao(db.Model):  # noqa: D101
    __tablename__ = "registry_admissao"
    id = Column(Integer, primary_key=True)
    data_solicitacao = Column(DateTime, nullable=False)
    prazo = Column(DateTime, nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    funcionario = db.relationship("Funcionarios", backref="registry_admissao")


class RegistryContrato(db.Model):  # noqa: D101
    id = Column(Integer, primary_key=True)
    contrato_name: str = Column(String(length=128))
    blob_doc = Column(LargeBinary(length=(2**32) - 1))
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"))
    funcionario = db.relationship("Funcionarios", backref="registry_contrato")


class FileModel(db.Model):  # noqa: D101
    __tablename__ = "file"
    id = Column(Integer, primary_key=True)
    filename = Column(String(length=128))
    secondary_filename = Column(String(length=128))
    filetype = Column(String(length=128))
    size = Column(Integer)
    mimetype = Column(String(length=128))
    mimetype_params = Column(JSON)
    blob = Column(LargeBinary(length=(2**32) - 1))
