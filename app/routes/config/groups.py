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


@config.route("/editar_grupo/<int:id>", methods=["GET", "POST"])
@login_required
def editar_grupo(id: int):
    """
    Handles the creation of a new group.
    Renders a form for creating a new group and processes the form submission.
    If the form is valid and the group does not already exist, a new group is created
    and added to the database along with its members.
    Returns:
        - On successful group creation, redirects to the groups configuration page.
        - On form validation failure or if the group already exists, re-renders the form with an error message.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    query = db.session.query(Groups).filter(Groups.id == id).first()
    choices = []
    for member in query.members:
        choices.extend([member.login])

    form = GroupForm(membros=choices, desc=query.description, nome=query.name_group)
    title = "Criar Grupo"
    page = "forms/GroupForm.html"

    if form.validate_on_submit():

        query.members.clear()
        query.name_group = form.nome.data
        query.description = form.desc.data

        for member in form.membros.data:

            usr = db.session.query(Users).filter(Users.login == member).first()
            query.members.append(usr)

        db.session.commit()

        flash("Grupo editado com sucesso!")
        return redirect("/config/groups")

    return render_template("index.html", page=page, form=form, title=title)
