import json
import os
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_user, logout_user

from app.forms import LoginForm
from app.models.users import Users

template_folder = os.path.join(Path(__file__).parent.resolve(), "templates")
auth = Blueprint("auth", __name__, template_folder=template_folder)


@auth.route("/", methods=["GET"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("dash.dashboard"))

    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    try:
        if session.get("_user_id", None) is not None:
            return redirect(url_for("dash.dashboard"))

        if not session.get("next"):
            session["next"] = request.args.get("next", url_for("dash.dashboard"))

        location = str(session.get("next"))
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(login=form.login.data).first()

            if user and user.converte_senha(form.password.data):
                session["username"] = form.login.data
                session["groups_usr"] = json.loads(user.grupos)
                session["nome_usuario"] = user.nome_usuario
                session.pop("next")
                login_user(user, remember=form.keep_login.data)
                flash("Login Efetuado com sucesso!", "success")

                if "?" in location:
                    location = location.split("?")[0]

                return redirect(location)

            flash("Usuário/Senha Incorretos!", "error")

        return render_template("login.html", form=form)

    except Exception as e:
        abort(500, description=str(e))


@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("Sessão encerrada", "info")
    location = url_for("auth.login")
    return redirect(location)
