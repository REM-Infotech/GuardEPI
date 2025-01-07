import json
from pathlib import Path
from flask import Response, abort
from flask import current_app as app
from flask import flash, redirect, render_template, session, make_response
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy


from ...forms import FormRoles
from ...models import Roles, Groups, Routes
from . import config


@config.route("/add_itens", methods=["GET", "POST"])
@login_required
def add_itens():

    try:

        form = FormRoles()

        rota = form.rota
        regras = form.permissoes

        item_role = {
            "ROTA": rota.data,
            "REGRAS": " - ".join(regra for regra in regras.data),
        }

        hex_name_json = session["json_filename"]
        path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
        json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

        with json_file.open("rb") as f:
            list_roles: list[dict[str, str | int]] = json.load(f)

        item_role.update({"ID": len(list_roles)})

        list_roles.append(item_role)
        json_obj = json.dumps(list_roles)

        with json_file.open("w") as f:
            f.write(json_obj)

        item_html = render_template("forms/roles/add_items.html", item=list_roles)

        # Retorna o HTML do item
        return item_html
    except Exception as e:
        abort(500, description=str(e))


@config.route("/remove-itens", methods=["GET", "POST"])
@login_required
def remove_itens():

    hex_name_json = session["json_filename"]
    path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
    json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

    with json_file.open("w") as f:
        f.write(json.dumps([]))

    item_html = render_template("form/roles/add_items.html")
    return item_html


@config.route("/roles", methods=["GET"])
@login_required
def roles() -> Response:
    try:

        title = "Regras"
        database = Roles.query.all()
        page = "roles.html"

        return make_response(
            render_template("index.html", title=title, database=database, page=page)
        )

    except Exception as e:
        abort(500, description=str(e))


@config.route("/cadastro_regra", methods=["GET", "POST"])
@login_required
def cadastro_regra() -> str | Response:
    """
    Handles the creation of a new group.
    Renders a form for creating a new group and processes the form submission.
    If the form is valid and the group does not already exist, a new group is created
    and added to the database along with its members.

    Returns:
        - On successful group creation, redirects to the Roles configuration page.
        - On form validation failure or if the group already exists, re-renders the form with an error message.
    """

    form = FormRoles()
    title = "Criar Grupo"
    page = "forms/roles/FormRoles.html"

    if form.validate_on_submit():

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        rulename = form.name_rule.data
        query = db.session.query(Roles).filter(Roles.name_role == rulename).first()

        routes_add = []

        if query:
            flash("Regra já existente!", "error")
            return render_template("index.html", page=page, form=form, title=title)

        new_ruleset = Roles(
            name_role=rulename,
            description=form.desc.data,
        )

        for group in form.grupos.data:

            grp = db.session.query(Groups).filter(Groups.name_group == group).first()
            new_ruleset.groups.append(grp)

        hex_name_json = session["json_filename"]
        path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
        json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

        with json_file.open("rb") as f:
            list_roles: list[dict[str, str | int]] = json.load(f)

        keys_routes = {}
        keys_routes.update(Routes.__dict__)

        lst_rm = list(keys_routes.keys())
        for key in lst_rm:
            if key.startswith("_"):
                keys_routes.pop(key)

        keys_routes.pop("id")
        keys_routes.pop("roles")
        keys_routes.pop("role_id")

        [keys_routes.pop(x) for x in ["CREATE", "READ", "UPDATE", "DELETE"]]

        for item in list_roles:
            to_add = keys_routes
            list_items = list(item.items())
            for key, value in list_items:
                if key == "ROTA":
                    to_add.update({"endpoint": value})
                    continue

                if key == "REGRAS":

                    for rule in value.split(" - "):
                        to_add.update({rule: True})

            routes_add.append(Routes(**to_add))

        db.session.add(new_ruleset)
        db.session.add_all(routes_add)

        db.session.commit()

        session.pop("json_filename")

        flash("Regra criada com sucesso")
        return redirect("/config/roles")

    return render_template("index.html", page=page, form=form, title=title)


# @config.route("/editar_regra/<int:id>", methods=["GET", "POST"])
# @login_required
# def editar_regra(id: int) -> str | Response:
#     """
#     Handles the creation of a new group.
#     Renders a form for creating a new group and processes the form submission.
#     If the form is valid and the group does not already exist, a new group is created
#     and added to the database along with its members.

#     Returns:
#         - On successful group creation, redirects to the Roles configuration page.
#         - On form validation failure or if the group already exists, re-renders the form with an error message.
#     """

#     db: SQLAlchemy = app.extensions["sqlalchemy"]

#     query = db.session.query(Roles).filter(Roles.id == id).first()
#     choices = []
#     for member in query.members:
#         choices.extend([member.login])

#     form = FormRoles(membros=choices, desc=query.description, nome=query.name_group)
#     title = "Criar Grupo"
#     page = "forms/roles/FormRoles.html"

#     if form.validate_on_submit():

#         query.members.clear()
#         query.name_group = form.nome.data
#         query.description = form.desc.data

#         for member in form.membros.data:

#             usr = db.session.query(Users).filter(Users.login == member).first()
#             query.members.append(usr)

#         db.session.commit()

#         flash("Grupo editado com sucesso!")
#         return redirect("/config/roles")

#     return render_template("index.html", page=page, form=form, title=title)


# import json
# import os
# import uuid

# from flask import flash, redirect, render_template, request, session, url_for
# from flask_login import login_required

# from app import app, db
# from app.decorators import create_perm
# from app.forms import FormRoles
# from app.models import Permissions


# @app.before_request
# def setPerms():

#     if request.endpoint == "Permissoes":
#         if not session.get("uuid_Permissoes", None):

#             session["uuid_Permissoes"] = str(uuid.uuid4())
#             pathj = os.path.join(
#                 app.config["TEMP_PATH"], f"{session["uuid_Permissoes"]}.json"
#             )

#             if os.path.exists(pathj):
#                 os.remove(pathj)

#             json_obj = json.dumps([])

#             with open(pathj, "w") as f:
#                 f.write(json_obj)


# @app.route("/add_itens_perms", methods=["GET", "POST"])
# @login_required
# def add_itens_perms():

#     form = FormRoles()
#     list = [form.rota.data, form.grupos.data, form.permissoes.data]

#     pathj = os.path.join(app.config["TEMP_PATH"], f"{session["uuid_Permissoes"]}.json")

#     with open(pathj, "rb") as f:
#         list_rules = json.load(f)

#     list_rules.append(list)
#     json_obj = json.dumps(list_rules)

#     with open(pathj, "w") as f:
#         f.write(json_obj)

#     item_html = render_template("includes/add_itens_perms.html", item=list_rules)

#     # Retorna o HTML do item
#     return item_html


# @app.route("/remove_itens_perms", methods=["GET", "POST"])
# @login_required
# def remove_itens_perms():

#     pathj = os.path.join(app.config["TEMP_PATH"], f"{session["uuid_Permissoes"]}.json")
#     json_obj = json.dumps([])

#     with open(pathj, "w") as f:
#         f.write(json_obj)

#     item_html = render_template("includes/add_items.html")
#     return item_html


# @app.route("/Permissoes", methods=["GET"])
# @login_required
# def Permissoes():

#     form = FormRoles()
#     page = f"{request.endpoint.lower()}.html"
#     title = request.endpoint.split(".")[1].capitalize()
#     database = Permissions.query.all()
#     return render_template(
#         "index.html", page=page, title=title, form=form, database=database
#     )


# @app.route("/create_role", methods=["POST"])
# @login_required
# @create_perm
# def create_role():

#     form = FormRoles()
#     perms = {}

#     pathj = os.path.join(app.config["TEMP_PATH"], f"{session["uuid_Permissoes"]}.json")

#     with open(pathj, "rb") as f:
#         list_rules = json.load(f)

#     if len(list_rules) == 0:
#         flash("Adicione ao menos uma regra!", "error")
#         return redirect(url_for("Permissoes"))

#     if form.validate_on_submit():

#         rule_name = form.name_rule.data

#         for rulecfg in list_rules:

#             rota = rulecfg[0]
#             rules = rulecfg[2]
#             perms.update({rota: rules})

#         dbase = Permissions.query.filter(
#             Permissions.name_rule == form.name_rule.data
#         ).first()

#         if not dbase:

#             rule = Permissions(
#                 name_rule=rule_name,
#                 Roles_members=json.dumps(form.grupos.raw_data),
#                 perms=json.dumps(perms),
#             )

#             db.session.add(rule)
#             db.session.commit()

#             flash("Regra criada com sucesso!", "success")
#             return redirect(url_for("Permissoes"))

#         flash("Regra com o mesmo nome já existe!", "error")

#     return redirect(url_for("Permissoes"))
