from app.models.Funcionários import *
from app.models.users import *
from app.models.EPI import *

from app import db
from app import app
from app.misc import generate_pid
import json

with app.app_context():

    db.create_all()
    to_add = []
    usr = Users.query.filter_by(login="root").first()

    if usr is None:

        usr = Users(

            grupos = json.dumps(["Grupo Root"]),
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
            name_group = "Grupo Root",
            members = json.dumps(["root", "nicholas@robotz.dev"]),
            perms = json.dumps({
            "Cautelas": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Departamentos": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Empresas": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Equipamentos": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Estoque": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Grade": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Estoque_Grade": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "Entradas": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "cargos": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "config": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "funcionarios": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            },
            "registros": {
                "permissoes": [
                    "CREATE",
                    "READ",
                    "UPDATE",
                    "DELETE"
                ]
            }
        }))
        to_add.append(grp)
        
        
    db.session.add_all(to_add)
    db.session.commit()