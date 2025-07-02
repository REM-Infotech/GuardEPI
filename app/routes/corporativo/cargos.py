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
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import CargoForm
from app.models import Cargos

from . import corp


@corp.route("/cargos")
@login_required
@read_perm
async def cargos():
    """
    Route to display the cargos page.
    This route is protected by login and will render the cargos page with data
    fetched from the Cargos database.
    Returns:
        Response: Renders the 'index.html' template with the cargos page and database data.
    Raises:
        HTTPException: If an error occurs, a 500 HTTP error is raised with the error description.
    """
    try:
        page = "cargos.html"
        database = Cargos.query.all()

        return await make_response(
            render_template(
                "index.html",
                page=page,
                database=database,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.route("/cargos/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastrar_cargos() -> Response:
    """
    Handles the creation and registration of new 'Cargos' (positions) in the system.
    This function processes a form submission for creating a new 'Cargo'. It validates the form,
    extracts the data, and adds a new entry to the database if the form is valid. Upon successful
    registration, it flashes a success message and redirects the user to the cargos page.
    Returns:
        Response: A redirect response to the cargos page if the form is successfully submitted and processed.
        Otherwise, it renders the form template for the user to fill out.
    Template:
        Renders 'index.html' with 'form_base.html' as the page content, passing the form, endpoint, and action.
    Flash Messages:
        Success: "Cargo cadastrado com sucesso!" - Displayed when a new cargo is successfully registered.
    """

    try:
        endpoint = "Cargos"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        form = CargoForm()
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if form.validate_on_submit():
            to_add = {}
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key.lower() == "csrf_token" or key.lower() == "submit":
                    continue

                to_add.update({key: value})

            item = Cargos(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Cargo cadastrado com sucesso!", "success")
            return await make_response(redirect(url_for("corp.cargos")))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.route("/cargos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
async def editar_cargos(id) -> Response:
    """
    Edits an existing position in the database.
    Args:
        id (int): The ID of the position to be edited.
    Returns:
        Response: Redirects to the positions page after a successful edit or renders the edit template.
    HTTP Methods:
        GET: Fills the form with the existing position data.
        POST: Validates and updates the position data in the database.
    Templates:
        index.html: Renders the position edit page with the filled form.
    Flash Messages:
        "Cargo editado com sucesso!": Displayed after a successful position edit.
    """

    try:
        endpoint = "cargos"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        cargos = db.session.query(Cargos).filter(Cargos.id == id).first()
        form = CargoForm(**cargos.__dict__)

        if form.validate_on_submit():
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key != "csrf_token" or key != "submit" and value:
                    setattr(cargos, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Cargo editado com sucesso!", "success")
            return await make_response(redirect(url_for("corp.cargos")))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.post("/cargos/deletar/<int:id>")
@login_required
@delete_perm
async def deletar_cargos(id: int) -> str:
    """
    Deletes a cargo record from the database based on the provided ID.
    Args:
        id (int): The ID of the cargo to be deleted.
    Returns:
        Response: Renders a template with a success message indicating that the cargo was deleted.
    Raises:
        sqlalchemy.orm.exc.NoResultFound: If no cargo with the given ID is found.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        cargos = db.session.query(Cargos).filter(Cargos.id == id).first()

        db.session.delete(cargos)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
