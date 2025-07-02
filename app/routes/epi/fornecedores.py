import traceback

from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from quart import (
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from app.forms import FornecedoresForm
from app.models import Fornecedores

from ...decorators import create_perm, delete_perm, read_perm, update_perm
from . import epi


@epi.route("/fornecedores", methods=["GET"])
@login_required
@read_perm
async def fornecedores() -> Response:
    """
    Renders the 'fornecedores' page with an empty database.
    This function sets the 'page' variable to "fornecedores.html" and initializes
    an empty list for the 'database'. It then renders the "index.html" template
    with the 'page' and 'database' variables.
    Returns:
        A rendered template of "index.html" with 'page' set to "fornecedores.html"
        and an empty 'database'.
    """

    try:
        title = "Fornecedores"
        page = "fornecedores.html"
        database = Fornecedores.query.all()
        return await make_response(
            await render_template(
                "index.html", page=page, database=database, title=title
            )
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/fornecedores/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastrar_fornecedores() -> Response:
    try:
        """
        Handles the registration of suppliers.
        This function processes the form submission for registering new suppliers.
        It validates the form data, adds the new supplier to the database, and
        commits the transaction. If the registration is successful, it flashes a
        success message and redirects to the suppliers page.
        Returns:
            Response: A redirect response to the suppliers page if the form is
            successfully submitted and processed. Otherwise, it renders the
            registration form template.
        """

        endpoint = "fornecedores"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        form = FornecedoresForm()
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if form.validate_on_submit():
            to_add = {}
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key.lower() == "csrf_token" or key.lower() == "submit":
                    continue

                to_add.update({key: value})

            item = Fornecedores(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            flash("Fornecedor cadastrado com sucesso!", "success")
            return await make_response(redirect(url_for("epi.fornecedores")))

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/fornecedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
async def editar_fornecedores(id: int) -> Response:
    """
    Edit a supplier's information in the database.
    This function handles the editing of supplier information based on the provided supplier ID.
    It supports both GET and POST requests. On a GET request, it populates the form with the
    supplier's current data. On a POST request, it validates the form and updates the supplier's
    information in the database if the form is valid.
    Args:
        id (int): The ID of the supplier to be edited.
    Returns:
        Response: A rendered template for the form on GET request, or a redirect to the suppliers
        list with a success message on successful form submission.
    """

    try:
        endpoint = "fornecedores"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = FornecedoresForm()

        fornecedor = (
            db.session.query(Fornecedores).filter(Fornecedores.id == id).first()
        )

        if request.method == "GET":
            form = FornecedoresForm(**fornecedor.__dict__)

        if form.validate_on_submit():
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key != "csrf_token" or key != "submit" and value:
                    setattr(fornecedor, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            flash("Fornecedor editado com sucesso!", "success")
            return await make_response(redirect(url_for("epi.fornecedores")))

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.post("/fornecedores/deletar/<int:id>")
@login_required
@delete_perm
async def deletar_fornecedores(id: int):
    """
    Deletes a supplier from the database based on the provided ID.
    Args:
        id (int): The ID of the supplier to be deleted.
    Returns:
        Response: A rendered template with a success message indicating that the supplier information has been successfully deleted.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        fornecedor = (
            db.session.query(Fornecedores).filter(Fornecedores.id == id).first()
        )

        db.session.delete(fornecedor)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
