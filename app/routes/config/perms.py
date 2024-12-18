# import json
# import os
# import uuid

# from flask import flash, redirect, render_template, request, session, url_for
# from flask_login import login_required

# from app import app, db
# from app.decorators import create_perm
# from app.forms import CreatePerm
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

#     form = CreatePerm()
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

#     form = CreatePerm()
#     page = f"pages/config/{request.endpoint.lower()}.html"
#     title = request.endpoint.split(".")[1].capitalize()
#     database = Permissions.query.all()
#     return render_template(
#         "index.html", page=page, title=title, form=form, database=database
#     )


# @app.route("/create_role", methods=["POST"])
# @login_required
# @create_perm
# def create_role():

#     form = CreatePerm()
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
#                 groups_members=json.dumps(form.grupos.raw_data),
#                 perms=json.dumps(perms),
#             )

#             db.session.add(rule)
#             db.session.commit()

#             flash("Regra criada com sucesso!", "success")
#             return redirect(url_for("Permissoes"))

#         flash("Regra com o mesmo nome já existe!", "error")

#     return redirect(url_for("Permissoes"))
