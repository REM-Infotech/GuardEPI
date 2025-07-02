import json
import traceback
from pathlib import Path

from quart import (
    Blueprint,
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from quart import current_app as app
from quart_auth import current_user, login_user, logout_user

from app.forms import LoginForm
from app.models.users import Users

template_folder = Path(__file__).parent.resolve().joinpath("templates")
auth = Blueprint("auth", __name__, template_folder=template_folder)


@auth.route("/", methods=["GET"])
async def index() -> Response:
    """
    Redirects the user based on their authentication status.
    If the current user is not authenticated, they are redirected to the dashboard.
    Otherwise, they are redirected to the login page.
    Returns:
        werkzeug.wrappers.Response: A redirect response to the appropriate URL.
    """

    try:
        if not current_user:
            return await make_response(redirect(url_for("auth.login")))
        return await make_response(redirect(url_for("dash.dashboard")))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@auth.route("/login", methods=["GET", "POST"])
async def login() -> Response:
    """
    Handle user login.
    This route handles the user login process. If the user is already logged in,
    they are redirected to the dashboard. If not, it processes the login form
    submission. On successful login, the user is redirected to the next page or
    the dashboard. If login fails, an error message is flashed.
    Returns:
        Response: A redirect to the appropriate page or the login template.
    Raises:
        HTTPException: If an exception occurs during the process, a 500 error is raised.
    """

    try:
        if session.get("_user_id", None) is not None:
            return await make_response(redirect(url_for("dash.dashboard")))

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

                return await make_response(redirect(location))

            flash("Usuário/Senha Incorretos!", "error")

        return await make_response(await render_template("login.html", form=form))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@auth.route("/logout", methods=["GET"])
async def logout() -> Response:
    """
    Logs out the current user, flashes a logout message, and redirects to the login page.
    This function performs the following actions:
    1. Logs out the current user using the `logout_user` function.
    2. Displays a flash message indicating that the session has ended.
    3. Redirects the user to the login page.
    Returns:
        Response: A redirect response object to the login page.
    """

    try:
        logout_user()
        flash("Sessão encerrada", "info")
        location = url_for("auth.login")
        return make_response(redirect(location))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)
