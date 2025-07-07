from datetime import datetime

import bcrypt
import pytz
from quart_auth import AuthUser as UserMixin
from sqlalchemy import Column, DateTime, Integer, LargeBinary, String

from app import db
from app.misc import generate_pid

salt = bcrypt.gensalt()

members = db.Table(
    "members",
    Column("users_id", Integer, db.ForeignKey("users.id"), primary_key=True),
    Column(
        "groups_id",
        Integer,
        db.ForeignKey("groups.id"),
        primary_key=True,
    ),
)

group_roles = db.Table(
    "group_roles",
    Column("roles_id", Integer, db.ForeignKey("roles.id"), primary_key=True),
    Column(
        "groups_id",
        Integer,
        db.ForeignKey("groups.id"),
        primary_key=True,
    ),
)

route_roles = db.Table(
    "route_roles",
    Column("roles_id", Integer, db.ForeignKey("roles.id"), primary_key=True),
    Column(
        "routes_id",
        Integer,
        db.ForeignKey("routes.id"),
        primary_key=True,
    ),
)


# @login_manager.user_loader
# def load_user(user_id):
#     link = request.referrer
#     if link is None:
#         link = request.url

#     return Users.query.get(int(user_id))


# @login_manager.request_loader
# async def request_loader(request: Request):
#     user_id = 0
#     return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(length=30), nullable=False, unique=True)
    nome_usuario = Column(String(length=64), nullable=False, unique=True)
    grupos = Column(String(length=1024), nullable=False)
    email = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=60), nullable=False)
    login_time = Column(DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4")))
    verification_code = Column(String(length=45), unique=True)
    login_id = Column(String(length=7), nullable=False, default=generate_pid())
    filename = Column(String(length=128))
    blob_doc = Column(LargeBinary(length=(2**32) - 1))

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.password = bcrypt.hashpw(senha_texto.encode(), salt).decode("utf-8")

    def converte_senha(self, senha_texto_claro) -> bool:
        return bcrypt.checkpw(
            senha_texto_claro.encode("utf-8"), self.password.encode("utf-8")
        )

    @property
    def auth_id(self) -> int:
        return self.id


class Groups(db.Model):
    __tablename__ = "groups"
    id: int = Column(Integer, primary_key=True)
    name_group = Column(String(length=30), nullable=False, unique=True)
    members = db.relationship("Users", secondary="members", backref="group")
    description = Column(String(length=128))


class Routes(db.Model):
    __tablename__ = "routes"
    id: int = Column(Integer, primary_key=True)
    endpoint = Column(String(length=32), nullable=False)
    roles = db.relationship("Roles", secondary="route_roles", backref="route")

    CREATE: bool = Column(db.Boolean, default=False)
    READ: bool = Column(db.Boolean, default=False)
    UPDATE: bool = Column(db.Boolean, default=False)
    DELETE: bool = Column(db.Boolean, default=False)


class Roles(db.Model):
    __tablename__ = "roles"
    id: int = Column(Integer, primary_key=True)
    name_role = Column(String(length=30), nullable=False, unique=True)
    groups = db.relationship("Groups", secondary="group_roles", backref="role")
    description = Column(String(length=128))
