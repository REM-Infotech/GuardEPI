from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from ...forms import GroupForm
from ...models import Groups, Users
from . import config


@config.route("/groups", methods=["GET"])
@login_required
def groups():
    try:

        title = "Grupos"
        database = Groups.query.all()
        page = "groups.html"

        return render_template("index.html", title=title, database=database, page=page)

    except Exception as e:
        abort(500, description=str(e))


@config.route("/cadastro_grupo", methods=["GET", "POST"])
@login_required
def cadastro_grupo():
    """
    Handles the creation of a new group.
    Renders a form for creating a new group and processes the form submission.
    If the form is valid and the group does not already exist, a new group is created
    and added to the database along with its members.
    Returns:
        - On successful group creation, redirects to the groups configuration page.
        - On form validation failure or if the group already exists, re-renders the form with an error message.
    """

    form = GroupForm()
    title = "Criar Grupo"
    page = "forms/GroupForm.html"

    if form.validate_on_submit():

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        query = (
            db.session.query(Groups).filter(Groups.name_group == form.nome.data).first()
        )

        if query:
            flash("Grupo já existente!", "error")
            return render_template("index.html", page=page, form=form, title=title)

        new_group = Groups(
            name_group=form.nome.data,
            description=form.desc.data,
        )

        for member in form.membros.data:

            usr = db.session.query(Users).filter(Users.login == member).first()
            new_group.members.append(usr)

        db.session.add(new_group)
        db.session.commit()

        flash("Grupo Criado com sucesso!")
        return redirect("/config/groups")

    return render_template("index.html", page=page, form=form, title=title)


# @config.route("/create_group", methods=["POST"])
# @login_required
# @create_perm
# def create_group():
#     form = GroupForm()
#     group = Groups.query.filter(Groups.name_group == form.nome.data).first()

#     if not group:
#         grp = Groups(name_group=form.nome.data, members=json.dumps(form.membros.data))

#         for usr in form.membros.data:
#             user = Users.query.filter(Users.login == usr).first()
#             list_group = json.loads(user.grupos)

#             for grupo in list_group:
#                 if grupo != form.nome.data:
#                     list_group.append(form.nome.data)
#                     break

#             user.grupos = json.dumps(list_group)

#         db.session.add(grp)
#         db.session.commit()
#         flash("Grupo criado com sucesso!")

#     else:
#         flash("Grupo já existente!", "error")

#     return redirect(url_for("groups", _scheme="https"))


# @config.route("/setEditGroup/<item>", methods=["GET"])
# @login_required
# # @update_perm
# def setEditGroup(item: int):
#     database = Groups.query.filter(Groups.id == item).first()
#     session["name_group"] = database.name_group

#     membros = []

#     if database.members:
#         membros = json.loads(database.members)

#     form = GroupForm(**{"nome": database.name_group, "membros": membros})

#     route = request.referrer.replace("https://", "").replace("http://", "")
#     route = route.split("/")[1]

#     grade_results = f"pages/forms/{route}/edit.html"
#     return render_template(grade_results, form=form, tipo=route, id=item)


# @config.route("/update_group", methods=["POST"])
# @login_required
# # @update_perm
# def update_group():
#     form = GroupForm()

#     gp_name = form.nome.data

#     if len(form.membros.data) == 0:
#         flash("Grupo requer ao menos 1 usuário", "error")
#         return redirect(url_for("groups", _scheme="https"))

#     # Query database grupo com o nome que está no Form
#     database = Groups.query.filter(Groups.name_group == gp_name).first()

#     # Se o nome não foi encontrado, ele foi alterado
#     if not database:
#         # Refaço a busca
#         database = Groups.query.filter(
#             Groups.name_group == session["name_group"]
#         ).first()

#     # Seto as alterações do database
#     database.name_group = gp_name
#     database.members = json.dumps(form.membros.data)

#     # Loop for nos membros do grupo
#     for usr in form.membros.data:
#         user = Users.query.filter(Users.login == usr).first()
#         list_group = json.loads(user.grupos)

#         # Se o usuário não está na lista de membros
#         if usr not in form.membros.data:
#             # Removo da lista de grupos na qual ele faz parte
#             list_group.remove(session["name_group"])

#         # Caso o grupo não esteja na lista de grupos no qual o usuário faz parte
#         elif form.nome.data not in list_group:
#             list_group.append(form.nome.data)

#         # Caso nome do grupo tenha sido alterado
#         if session["name_group"] != form.nome.data:
#             list_group.remove(session["name_group"])
#             list_group.append(form.nome.data)

#         user.grupos = json.dumps(list_group)

#     db.session.commit()

#     flash("Alterações salvas com sucesso!")
#     return redirect(url_for("groups", _scheme="https"))


# @config.route("/deleteGroup/<id>", methods=["POST"])
# @login_required
# @delete_perm
# def deleteGroup(id: int):
#     template = "includes/show.html"

#     # Query do grupo a ser deletado
#     dbase_group = Groups.query.filter(Groups.id == id).first()
#     nome_grupo: str = dbase_group.name_group

#     # Se o grupo a ser deletado for root, ele vai bloquear
#     if nome_grupo == "Grupo Root":
#         message = "Grupo Root não pode ser deletado!"
#         return render_template(template, message=message)

#     # Loop for nos membros
#     for user in json.loads(dbase_group.members):
#         # Query do user
#         query_user = Users.query.filter(Users.login == user).first()

#         # Se o usuário nao existir, continua
#         if not query_user:
#             continue

#         # Ver os grupos no qual o usuário está
#         list_grupos = json.loads(query_user.grupos)

#         for grupo in list_grupos:
#             # Se o grupo a ser deletado estiver na lista
#             if grupo == nome_grupo:
#                 # Remove o grupo da lista de grupos que o usuário faz parte
#                 list_grupos.remove(grupo)
#                 break

#         # Atualiza a lista de grupos do usuário
#         query_user.grupos = json.dumps(list_grupos)
#         db.session.commit()

#     db.session.delete(dbase_group)
#     db.session.commit()

#     message = "Grupo deletado com sucesso!"
#     return render_template(template, message=message)
