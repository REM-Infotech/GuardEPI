import json

from flask import abort
from flask import current_app as app
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
)
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers.response import Response

from ...decorators import create_perm, delete_perm, read_perm, update_perm

from ...forms import AdmChangeEmail, AdmChangePassWord, FormUser
from ...models import Users
from . import config


@config.get("/users")
@login_required
@read_perm
def users() -> Response:
    try:

        database = Users.query.order_by(Users.login_time.desc()).all()
        title = "Usuários"
        page = "users.html"
        return make_response(
            render_template("index.html", title=title, database=database, page=page)
        )

    except Exception as e:
        abort(500, description=str(e))


@config.route("/cadastro_usuario", methods=["GET", "POST"])
@login_required
@create_perm
def cadastro_usuario() -> str | Response | None:
    form = FormUser()
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        html = "forms/FormUser.html"
        return render_template(html, form=form)

    elif request.method == "POST" and form.validate_on_submit():

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        usuario = Users(
            login=form.login.data,
            nome_usuario=form.nome.data,
            email=form.email.data,
            grupos=json.dumps(["Default"]),
        )

        usuario.senhacrip = form.password.data

        try:
            db.session.add(usuario)
            db.session.commit()

            flash("Usuário criado com sucesso!", "success")
            return redirect(url_for("config.users"))

        except Exception as e:
            abort(500, description=str(e))

    else:
        if form.errors:
            pass

        else:
            return redirect(url_for("config.users"))


@config.route("/changepw_usr", methods=["GET", "POST"])
@login_required
@update_perm
def changepw_usr() -> Response | str:
    try:
        form = AdmChangePassWord()

        html = "forms/ChangePasswordForm.html"

        if form.validate_on_submit():

            db: SQLAlchemy = app.extensions["sqlalchemy"]
            if form.new_password.data != form.repeat_password.data:
                flash("Senhas não coincidem")
                return redirect(url_for("config.users"))

            login_usr = form.data.get("user_to_change", session.get("login"))
            password = Users.query.filter_by(login=login_usr).first()
            password.senhacrip = form.new_password.data
            db.session.commit()

            flash("Senha alterada com sucesso!", "success")
            return redirect(url_for("config.users"))

        return render_template(html, form=form)

    except Exception as e:
        abort(500, description=str(e))


@config.route("/changemail_usr", methods=["GET", "POST"])
@login_required
@update_perm
def changemail_usr() -> Response | str:
    try:
        form = AdmChangeEmail()

        html = "forms/ChangeMailForm.html"

        if form.validate_on_submit():

            db: SQLAlchemy = app.extensions["sqlalchemy"]
            login_usr = form.data.get("user_to_change", session.get("login"))
            mail = Users.query.filter_by(login=login_usr).first()
            if form.new_email.data != form.repeat_email.data:
                flash("E-mails não coincidem")
                return redirect(url_for("config.users"))

            mail.email = form.new_email.data
            db.session.commit()

            flash("E-mail alterado com sucesso!", "success")
            return redirect(url_for("config.users"))

        return render_template(html, form=form)

    except Exception as e:
        abort(500, description=str(e))


@config.route("/delete_user/<usuario>", methods=["GET"])
@login_required
@delete_perm
def delete_user(usuario: str) -> str:
    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        set_delete = True

        atual_admin = session.get("username")
        # license_key = session.get("license_token", "")

        message = ""
        query = db.session.query(Users).filter(Users.login == usuario).first()
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
        return render_template(template, message=message)

    except Exception as e:
        abort(500, description=str(e))
