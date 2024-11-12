from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from .Funcionários import Funcionarios, Cargos, Departamento, Empresa
from .users import Users, Groups, EndPoints
from .EPI import (
    RegistrosEPI,
    ProdutoEPI,
    EstoqueEPI,
    EstoqueGrade,
    GradeEPI,
    RegistroEntradas,
)

from app.misc import generate_pid
import json

from app.defaults import perms_root, perms_default

endpoints = [
    ("registros", "Registros"),
    ("users", "Usuários"),
    ("groups", "Grupos"),
    ("set1", "Produtos"),
    ("Equipamentos", "Info. Equipamentos"),
    ("Grade", "Info. Grade"),
    ("set2", "Estoque"),
    ("Estoque", "Equipamentos"),
    ("Estoque_Grade", "Grades"),
    ("Entradas", "Entradas"),
    ("Cautelas", "Cautelas"),
    ("funcionarios", "Funcionários"),
    ("Empresas", "Empresas"),
    ("cargos", "Cargos"),
    ("Departamentos", "Departamentos"),
]

__all__ = [
    Funcionarios,
    Departamento,
    Cargos,
    Empresa,
    Users,
    Groups,
    EndPoints,
    RegistrosEPI,
    ProdutoEPI,
    EstoqueEPI,
    EstoqueGrade,
    GradeEPI,
    RegistroEntradas,
]


def init_database(app: Flask, db: SQLAlchemy) -> None:

    with app.app_context():

        db.create_all()
        to_add = []
        usr = Users.query.filter_by(login="root").first()

        if usr is None:

            usr = Users(
                grupos=json.dumps(["Grupo Root"]),
                login="root",
                nome_usuario="Root",
                email="nicholas@robotz.dev",
            )
            root_pw = generate_pid(10)
            usr.senhacrip = root_pw
            print(f"* Root Pw: {root_pw}")
            to_add.append(usr)

        group = Groups.query.filter(Groups.name_group == "Grupo Root").first()

        if group is None:

            grp = Groups(
                name_group="Grupo Root",
                members=json.dumps(["root", "nicholas@robotz.dev"]),
                perms=json.dumps(perms_root),
            )
            to_add.append(grp)

        group = Groups.query.filter(Groups.name_group == "Default").first()

        if group is None:
            grp = Groups(
                name_group="Default",
                members=json.dumps(["nicholas@robotz.dev"]),
                perms=json.dumps(perms_default),
            )
            to_add.append(grp)

        for endpoint, displayName in endpoints:

            checkend = EndPoints.query.filter(EndPoints.endpoint == endpoint).first()

            if not checkend:

                add = EndPoints(endpoint=endpoint, displayName=displayName)

                to_add.append(add)

        db.session.add_all(to_add)
        db.session.commit()
