from datetime import datetime

import bcrypt
import pytz
from flask import request
from flask_login import UserMixin

from app import db, login_manager
from app.misc import generate_pid

salt = bcrypt.gensalt()

members = db.Table(
    "members",
    db.Column("users_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column(
        "groups_id",
        db.Integer,
        db.ForeignKey("groups.id"),
        primary_key=True,
    ),
)

group_roles = db.Table(
    "group_roles",
    db.Column("roles_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "groups_id",
        db.Integer,
        db.ForeignKey("groups.id"),
        primary_key=True,
    ),
)

route_roles = db.Table(
    "route_roles",
    db.Column("roles_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
    db.Column(
        "routes_id",
        db.Integer,
        db.ForeignKey("routes.id"),
        primary_key=True,
    ),
)


@login_manager.user_loader
def load_user(user_id):
    link = request.referrer
    if link is None:
        link = request.url

    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):

    __tablename__ = "users"
    id: int = db.Column(db.Integer, primary_key=True)
    login: str = db.Column(db.String(length=30), nullable=False, unique=True)
    nome_usuario: str = db.Column(db.String(length=64), nullable=False, unique=True)
    grupos: str = db.Column(db.String(length=1024), nullable=False)
    email: str = db.Column(db.String(length=50), nullable=False, unique=True)
    password: str = db.Column(db.String(length=60), nullable=False)
    login_time: datetime = db.Column(
        db.DateTime, default=datetime.now(pytz.timezone("Etc/GMT+4"))
    )
    verification_code: str = db.Column(db.String(length=45), unique=True)
    login_id: str = db.Column(
        db.String(length=7), nullable=False, default=generate_pid()
    )
    filename: str = db.Column(db.String(length=128))
    blob_doc: str = db.Column(db.LargeBinary(length=(2**32) - 1))

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


class Groups(db.Model):

    __tablename__ = "groups"
    id: int = db.Column(db.Integer, primary_key=True)
    name_group: str = db.Column(db.String(length=30), nullable=False, unique=True)
    members = db.relationship("Users", secondary="members", backref="group")
    description: str = db.Column(db.String(length=128))


class Routes(db.Model):

    __tablename__ = "routes"
    id: int = db.Column(db.Integer, primary_key=True)
    endpoint: str = db.Column(db.String(length=32), nullable=False)
    roles = db.relationship("Roles", secondary="route_roles", backref="route")

    CREATE: bool = db.Column(db.Boolean, default=False)
    READ: bool = db.Column(db.Boolean, default=False)
    UPDATE: bool = db.Column(db.Boolean, default=False)
    DELETE: bool = db.Column(db.Boolean, default=False)


class Roles(db.Model):

    __tablename__ = "roles"
    id: int = db.Column(db.Integer, primary_key=True)
    name_role: str = db.Column(db.String(length=30), nullable=False, unique=True)
    groups = db.relationship("Groups", secondary="group_roles", backref="role")
    description: str = db.Column(db.String(length=128))
