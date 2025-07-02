import traceback  # traceback

from flask_sqlalchemy import SQLAlchemy
from quart import Response, abort, flash, make_response, redirect, render_template
from quart import current_app as app
from quart_auth import login_required

from app.decorators import create_perm, read_perm

from ...forms import GroupForm
from ...models import Groups, Roles, Users
from . import config


@config.route("/groups", methods=["GET"])
@login_required
@read_perm
def groups() -> Response:
    try:
        title = "Grupos"
        database = Groups.query.all()
        page = "groups.html"

        return await make_response(
            render_template("index.html", title=title, database=database, page=page)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/cadastro_grupo", methods=["GET", "POST"])
@login_required
@create_perm
def cadastro_grupo() -> Response:
    try:
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
                db.session.query(Groups)
                .filter(Groups.name_group == form.nome.data)
                .first()
            )

            if query:
                flash("Grupo já existente!", "error")
                return await make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

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
            return await make_response(redirect("/config/groups"))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/editar_grupo/<int:id>", methods=["GET", "POST"])
@login_required
def editar_grupo(id: int) -> Response:
    try:
        """
        Handles the creation of a new group.
        Renders a form for creating a new group and processes the form submission.
        If the form is valid and the group does not already exist, a new group is created
        and added to the database along with its members.
        Returns:
            - On successful group creation, redirects to the groups configuration page.
            - On form validation failure or if the group already exists, re-renders the form with an error message.
        """

        title = "Criar Grupo"
        page = "forms/GroupForm.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        query = db.session.query(Groups).filter(Groups.id == id).first()
        choices = []
        for member in query.members:
            choices.extend([member.login])

        form = GroupForm(membros=choices, desc=query.description, nome=query.name_group)

        if form.validate_on_submit():
            query.members.clear()
            query.name_group = form.nome.data
            query.description = form.desc.data

            for member in form.membros.data:
                usr = db.session.query(Users).filter(Users.login == member).first()
                query.members.append(usr)

            db.session.commit()

            flash("Grupo editado com sucesso!")
            return await make_response(redirect("/config/groups"))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.get("/deletar_grupo/<int:id>")
@login_required
def deletar_grupo(id: int) -> Response:
    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        from_users = (
            db.session.query(Users)
            .select_from(Groups)
            .join(Groups.members)
            .filter(Groups.id == id)
            .all()
        )

        from_roles = (
            db.session.query(Roles)
            .select_from(Groups)
            .join(Groups.role)
            .filter(Groups.id == id)
            .all()
        )

        group = db.session.query(Groups).filter(Groups.id == id).first()

        for role in from_roles:
            role.groups.remove(group)

        for user in from_users:
            user.group.remove(group)

        db.session.delete(group)
        db.session.commit()

        message = "Grupo deletado com sucesso!"
        template = "includes/show.html"

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar grupo"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
