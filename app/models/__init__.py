from app.models.Funcionários import *
from app.models.users import *
from app.models.EPI import *

from app import db
from app import app
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
    ("Departamentos", "Departamentos")
]


def init_database() -> None:

    with app.app_context():

        db.create_all()
        to_add = []
        usr = Users.query.filter_by(login="root").first()

        if usr is None:
            
            filename = "favicon.png"
            path_img = os.path.join("app/src/assets/img", filename)
            with open(path_img, 'rb') as file:
                blob_doc = file.read()
            usr = Users(

                grupos=json.dumps(["Grupo Root"]),
                login="root",
                nome_usuario="Root",
                email="nicholas@robotz.dev",
                blob_doc = blob_doc,
                filename = filename)
            root_pw = generate_pid(10)
            usr.senhacrip = root_pw
            print(f"* Root Pw: {root_pw}")
            to_add.append(usr)

        group = Groups.query.filter(Groups.name_group == "Grupo Root").first()

        if group is None:

            grp = Groups(
                name_group="Grupo Root",
                members=json.dumps(["root", "nicholas@robotz.dev", "nicholas.silva"]),
                perms=json.dumps(perms_root))
            to_add.append(grp)
            
        else:
            group.perms = json.dumps(perms_root)

        group = Groups.query.filter(Groups.name_group == "Default").first()

        if group is None:
            grp = Groups(
                name_group="Default",
                members=json.dumps(["nicholas@robotz.dev"]),
                perms=json.dumps(perms_default)
            )
            to_add.append(grp)
            
        else:
            group.perms = json.dumps(perms_root)

        for endpoint, displayName in endpoints:

            checkend = EndPoints.query.filter(
                EndPoints.endpoint == endpoint).first()

            if not checkend:

                add = EndPoints(

                    endpoint=endpoint,
                    displayName=displayName
                )
                
                to_add.append(add)

        if len(to_add) > 0:
            db.session.add_all(to_add)
        
        try:
            db.session.commit()
        except:
            pass
