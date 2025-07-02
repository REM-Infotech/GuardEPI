# noqa: D100, D104

import bcrypt
from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from app import db

salt = bcrypt.gensalt()


class Funcionarios(db.Model):  # noqa: D101
    __tablename__ = "funcionarios"
    id = Column(Integer, primary_key=True)
    # Dados de login
    nome = Column(String(length=64))
    email = Column(String(length=64))
    password = Column(String(length=60))
    data_admissao = Column(DateTime)
    login_time = Column(DateTime)
    verification_code = Column(String(length=45), unique=True)
    login_id = Column(String(length=64))
    filename = Column(String(length=128))
    blob_doc = Column(LargeBinary(length=(2**32) - 1))
    status_admissao = Column(String(length=64), default="PENDENTE")
    # Dados de cadastro
    codigo = Column(String(length=6), unique=True)
    deficiencia = Column(String(length=64))
    cargo = Column(String(length=64))
    departamento = Column(String(length=64))
    empresa = Column(String(length=64))
    cpf = Column(String(length=14), unique=True)

    @property
    def senhacrip(self) -> any:
        """
        Get the encrypted password.

        Returns:
            str: The encrypted password.

        """
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto: str) -> None:
        """
        Encrypt and set the user’s password.

        Args:
            senha_texto (str): Plain text password.

        """
        self.password = bcrypt.hashpw(senha_texto.encode(), salt).decode("utf-8")

    def check_password(self, senha_texto_claro: str) -> bool:
        """
        Check if the provided password matches the stored encrypted password.

        Args:
            senha_texto_claro (str): Plain text password.

        Returns:
            bool: True if valid, False otherwise.

        """
        return bcrypt.checkpw(
            senha_texto_claro.encode("utf-8"), self.password.encode("utf-8")
        )


class Cargos(db.Model):  # noqa: D101
    id = Column(Integer, primary_key=True)
    cargo = Column(String(length=64), nullable=False, unique=True)
    descricao = Column(String(length=512))


class Departamento(db.Model):  # noqa: D101
    __tablename__ = "departamentos"
    id = Column(Integer, primary_key=True)
    departamento = Column(String(length=64), nullable=False, unique=True)
    descricao = Column(String(length=512))


class Empresa(db.Model):  # noqa: D101
    __tablename__ = "empresa"
    id: int = Column(Integer, primary_key=True)
    nome_empresa = Column(String(length=64), unique=True)
    cnpj_empresa = Column(String(length=64), unique=True)
    filename = Column(String(length=128))
    blob_doc = Column(LargeBinary(length=(2**32) - 1))
