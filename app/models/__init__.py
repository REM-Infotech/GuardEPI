import json
import os

from dotenv import dotenv_values

from app import app, db
from app.misc import generate_pid

from .EPI import (
    ClassesEPI,
    EstoqueEPI,
    EstoqueGrade,
    Fornecedores,
    GradeEPI,
    Marcas,
    ModelosEPI,
    ProdutoEPI,
    RegistroEntradas,
    RegistroSaidas,
    RegistrosEPI,
)
from .Funcionários import Cargos, Departamento, Empresa, Funcionarios
from .users import EndPoints, Groups, Permissions, Users

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
    ("cargo_bp.cargos", "cargo_bp.cargos"),
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


def init_database() -> str:
    root_pw = generate_pid(10)

    with app.app_context():
        db.create_all()
        to_add = []

        values = dotenv_values()

        loginsys = values.get("loginsys")
        nomeusr = values.get("nomeusr")
        emailusr = values.get("emailusr")

        usr = db.session.query(Users).filter_by(login=loginsys).first()

        if usr is None:
            filename = "favicon.png"
            path_img = os.path.join("app", "src", "assets", "img", filename)
            with open(path_img, "rb") as file:
                blob_doc = file.read()
            usr = Users(
                grupos=json.dumps(["Grupo Root"]),
                login=loginsys,
                nome_usuario=nomeusr,
                email=emailusr,
                blob_doc=blob_doc,
                filename=filename,
            )

            usr.senhacrip = root_pw
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

        # Issue: [B110:try_except_pass] Try, Except, Pass detected.
        # Severity: Low   Confidence: High
        # CWE: CWE-703 (https://cwe.mitre.org/data/definitions/703.html)
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # try:
        #     db.session.commit()
        # except Exception:
        #     pass
        try:
            db.session.commit()
        except Exception as e:
            raise e

    return f" * Root Pw: {root_pw}"
