import json
from os import path
from pathlib import Path

from dotenv import dotenv_values
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
from .users import Groups, Roles, Routes, Users

__all__ = (
    Funcionarios,
    Empresa,
    Cargos,
    Departamento,
    Routes,
    Roles,
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

endpoints = ["/epi", "/corp", "/config", "/estoque"]


def init_database(app: Flask, db: SQLAlchemy) -> str:

    with app.app_context():

        db.create_all()

        to_add = []

        values = dotenv_values()

        loginsys = values.get("loginsys")
        nomeusr = values.get("nomeusr")
        emailusr = values.get("emailusr")

        root_pw = generate_pid(10)
        usr = db.session.query(Users).filter_by(login=loginsys).first()

        if usr is None:
            filename = "favicon.png"
            path_img = Path(app.static_folder).joinpath(
                path.join("assets", "img", filename)
            )

            with path_img.open("rb") as file:
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

        group = (
            db.session.query(Groups).filter(Groups.name_group == "Grupo Root").first()
        )

        if group is None:
            group = Groups(name_group="Grupo Root")
            group.members.append(usr)

            role = db.session.query(Roles).filter(Roles.name_role == "Root").first()
            if role is None:
                role = Roles(name_role="Root")
                role.groups.append(group)

                for endpoint in endpoints:
                    route = Routes(endpoint=endpoint)
                    route.CREATE = True
                    route.READ = True
                    route.UPDATE = True
                    route.DELETE = True
                    route.roles = role
                    to_add.append(route)

                to_add.append(role)

            to_add.append(group)

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
