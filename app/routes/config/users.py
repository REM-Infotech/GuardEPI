import json
import traceback

from flask_sqlalchemy import SQLAlchemy
from quart import (
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    session,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from ...decorators import create_perm, delete_perm, read_perm, update_perm
from ...forms import AdmChangeEmail, AdmChangePassWord, FormUser
from ...models import Users
from . import config


@config.get("/users")
@login_required
@read_perm
async def users() -> Response:
    try:
        title = "Usuários"
        page = "users.html"

        database = Users.query.order_by(Users.login_time.desc()).all()

        return await make_response(
            render_template("index.html", title=title, database=database, page=page)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/cadastro_usuario", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastro_usuario() -> Response:
    form = FormUser()
    html = "forms/FormUser.html"

    try:
        if form.validate_on_submit():
            db: SQLAlchemy = app.extensions["sqlalchemy"]

            if db.session.query(Users).filter(Users.login == form.login.data).first():
                flash("Já existe um usuário com este login!")
                return await make_response(redirect(url_for("config.users")))

            usuario = Users(
                login=form.login.data,
                nome_usuario=form.nome.data,
                email=form.email.data,
                grupos=json.dumps(["Default"]),
            )

            usuario.senhacrip = form.password.data

            db.session.add(usuario)
            db.session.commit()

            flash("Usuário criado com sucesso!", "success")
            return await make_response(redirect(url_for("config.users")))

        if form.errors:
            flash(form.errors)

        return await make_response(render_template(html, form=form))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)

    return await make_response(render_template(html))


@config.route("/changepw_usr", methods=["GET", "POST"])
@login_required
@update_perm
async def changepw_usr() -> Response:
    html = "forms/ChangePasswordForm.html"
    try:
        form = AdmChangePassWord()

        if form.validate_on_submit():
            db: SQLAlchemy = app.extensions["sqlalchemy"]
            if form.new_password.data != form.repeat_password.data:
                flash("Senhas não coincidem")
                return await make_response(redirect(url_for("config.users")))

            login_usr = form.data.get("user_to_change", session.get("login"))
            password = Users.query.filter_by(login=login_usr).first()
            password.senhacrip = form.new_password.data
            db.session.commit()

            flash("Senha alterada com sucesso!", "success")
            return await make_response(redirect(url_for("config.users")))

        return await make_response(render_template(html, form=form))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)

    return await make_response(render_template(html))


@config.route("/changemail_usr", methods=["GET", "POST"])
@login_required
@update_perm
async def changemail_usr() -> Response:
    html = "forms/ChangeMailForm.html"
    try:
        form = AdmChangeEmail()

        if form.validate_on_submit():
            db: SQLAlchemy = app.extensions["sqlalchemy"]
            login_usr = form.data.get("user_to_change", session.get("login"))
            mail = Users.query.filter_by(login=login_usr).first()
            if form.new_email.data != form.repeat_email.data:
                flash("E-mails não coincidem")
                return await make_response(redirect(url_for("config.users")))

            mail.email = form.new_email.data
            db.session.commit()

            flash("E-mail alterado com sucesso!", "success")
            return await make_response(redirect(url_for("config.users")))

        return await make_response(render_template(html, form=form))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)

    return await make_response(render_template(html, form=form))


@config.route("/delete_user/<id>", methods=["GET"])
@login_required
@delete_perm
async def delete_user(id: int) -> Response:
    """
    Deletes a user from the database based on the provided user ID.

    This function performs the following steps:
    1. Retrieves the SQLAlchemy database extension from the app.
    2. Checks if the current user is the same as the user to be deleted.
    3. If the current user is not the same as the user to be deleted, deletes the user from the database.
    4. Commits the transaction to the database.
    5. Returns a success message if the user is deleted, or an error message if the user cannot be deleted.

    Args:
        id (int): The ID of the user to be deleted.
    Returns:
        str: A message indicating the result of the deletion operation.
    Raises:
        HTTPException: If an error occurs during the deletion process, a 500 HTTP error is raised with the error description.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        set_delete = True

        atual_admin: str = session.get("username")
        # license_key = session.get("license_token", "")

        message = ""
        query = db.session.query(Users).filter(Users.id == id).first()
        usuario = query.login

        # if session.get("tipo-usuario") == "super_admin":

        # elif session.get("tipo-usuario") == "admin":
        #     query = Users.query.filter(Users.license_key == license_key).all()
        userto_delete = query
        message = "Usuário deletado com sucesso!"

        if usuario == atual_admin:
            message = "Você nao pode deletar seu usuário"
            set_delete = False

        if set_delete is True:
            db.session.delete(userto_delete)
            db.session.commit()

        template = "includes/show.html"
        return await make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
