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
    nome = Column(String)
    cpf = Column(String)
    email = Column(String)
    data_nascimento = Column(String)
    telefone = Column(String)
    endereco = Column(String)
    complemento = Column(String)
    cidade = Column(String)
    cep = Column(String)
    estado = Column(String)
    genero = Column(String)
    corRaca = Column(String)  # noqa: N815
    grauEscolaridade = Column(String)  # noqa: N815
    estadoCivil = Column(String)  # noqa: N815
    numero_residencia = Column(String)

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
    filename = Column(String)
    secondary_filename = Column(String)
    filetype = Column(String)
    size = Column(Integer)
    mimetype = Column(String)
    mimetype_params = Column(JSON)
    blob = Column(LargeBinary)
