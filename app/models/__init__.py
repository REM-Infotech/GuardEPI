from .Funcionários import Funcionarios, Empresa, Cargos, Departamento
from .users import Users, Groups, Permissions, EndPoints
from .EPI import (
    ProdutoEPI,
    EstoqueEPI,
    EstoqueGrade,
    Marcas,
    GradeEPI,
    ClassesEPI,
    ModelosEPI,
    Fornecedores,
    RegistroEntradas,
    RegistroSaidas,
    RegistrosEPI,
)

import os
from app import db
from app import app
from app.misc import generate_pid
import json


endpoints = [
    ("Equipamentos", "Equipamentos"),
    ("Fornecedores", "Fornecedores"),
    ("Marcas", "Marcas"),
    ("Modelos", "Modelos"),
    ("Classes", "Classes"),
    ("Estoque", "Estoque"),
    ("Estoque_Grade", "Estoque_Grade"),
    ("Entradas", "Entradas"),
    ("Registro_Saidas", "Registro_Saidas"),
    ("Cautelas", "Cautelas"),
    ("Grade", "Grade"),
    ("cargos", "cargos"),
    ("Empresas", "Empresas"),
    ("funcionarios", "funcionarios"),
    ("Departamentos", "Departamentos"),
    ("users", "users"),
    ("groups", "groups"),
    ("Permissoes", "Permissoes"),
]

__all__ = (
    Funcionarios,
    Empresa,
    Cargos,
    Departamento,
    Permissions,
    ProdutoEPI,
    EstoqueEPI,
    EstoqueGrade,
    Marcas,
    GradeEPI,
    ClassesEPI,
    ModelosEPI,
    Fornecedores,
    RegistroEntradas,
    RegistroSaidas,
    RegistrosEPI,
)


def init_database() -> None:

    with app.app_context():

        db.create_all()
        to_add = []
        usr = Users.query.filter_by(login="root").first()

        if usr is None:

            filename = "favicon.png"
            path_img = os.path.join("app/src/assets/img", filename)
            with open(path_img, "rb") as file:
                blob_doc = file.read()
            usr = Users(
                grupos=json.dumps(["Grupo Root"]),
                login="root",
                nome_usuario="Root",
                email="adm@robotz.dev",
                blob_doc=blob_doc,
                filename=filename,
            )

            root_pw = generate_pid(10)
            usr.senhacrip = root_pw
            print(f" * Root Pw: {root_pw}")
            to_add.append(usr)

        group = Groups.query.filter(Groups.name_group == "Grupo Root").first()

        if group is None:

            grp = Groups(name_group="Grupo Root", members=json.dumps(["root"]))
            to_add.append(grp)

        group = Groups.query.filter(Groups.name_group == "Default").first()

        if group is None:
            grp = Groups(name_group="Default")
            to_add.append(grp)

        for endpoint, displayName in endpoints:

            checkend = EndPoints.query.filter(EndPoints.endpoint == endpoint).first()

            if not checkend:

                add = EndPoints(endpoint=endpoint, displayName=displayName)

                to_add.append(add)

        if len(to_add) > 0:
            db.session.add_all(to_add)

        try:
            db.session.commit()
        except Exception:
            pass
