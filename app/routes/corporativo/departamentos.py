import traceback

from flask_login import login_required
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

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import FormDepartamentos
from app.models import Departamento

from . import corp


@corp.route("/Departamentos")
@login_required
@read_perm
def Departamentos() -> Response:
    """
    Handles the route for displaying the departments page.
    This function queries all departments from the database and renders the
    'index.html' template with the departments data. If an exception occurs
    during the process, it aborts the request with a 500 status code and
    includes the exception message in the response.
    Returns:
        Response: A Quart response object that renders the 'index.html' template
        with the departments data.
    Raises:
        HTTPException: If an exception occurs, a 500 HTTP status code is returned
        with the exception message.
    """

    try:
        page = "departamentos.html"
        database = Departamento.query.all()

        return make_response(
            render_template(
                "index.html",
                page=page,
                database=database,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.route("/Departamentos/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
def cadastrar_departamentos() -> Response:
    """
    Handles the creation and registration of new departments.
    This function processes a form submission for creating new departments.
    It validates the form data, adds the new department to the database,
    and commits the transaction. If the form submission is successful,
    it flashes a success message and redirects to the departments page.
    Returns:
        Response: A redirect response to the departments page if the form is successfully submitted,
                  otherwise renders the form template for department registration.
    """

    try:
        endpoint = "Departamentos"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        form = FormDepartamentos()

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if form.validate_on_submit():
            to_add = {}
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key.lower() == "csrf_token" or key.lower() == "submit":
                    continue

                to_add.update({key: value})

            item = Departamento(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Departamentos cadastrada com sucesso!", "success")
            return make_response(redirect(url_for("corp.Departamentos")))

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.route("/Departamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
def editar_departamentos(id) -> Response:
    """
    Edit a department by its ID.
    This function handles the editing of a department's details. It retrieves the department
    from the database using the provided ID, populates a form with the department's current
    details, and updates the department's information if the form is submitted and validated.
    Args:
        id (int): The ID of the department to be edited.
    Returns:
        Response: A rendered template for the department edit form, or a redirect to the
        department list page if the form is successfully submitted and processed.
    """

    try:
        endpoint = "Departamentos"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        Departamentos = (
            db.session.query(Departamento).filter(Departamento.id == id).first()
        )
        form = FormDepartamentos(**Departamentos.__dict__)

        if form.validate_on_submit():
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key != "csrf_token" or key != "submit" and value:
                    setattr(Departamentos, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Departamentos editada com sucesso!", "success")
            return make_response(redirect(url_for("corp.Departamentos")))

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.post("/Departamentoss/deletar/<int:id>")
@login_required
@delete_perm
def deletar_departamentos(id: int) -> Response:
    """
    Deletes a department from the database based on the provided ID.
    Args:
        id (int): The ID of the department to be deleted.
    Returns:
        Response: Renders a template with a success message indicating that the information was successfully deleted.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        Departamentos = (
            db.session.query(Departamento).filter(Departamento.id == id).first()
        )

        db.session.delete(Departamentos)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return make_response(render_template(template, message=message))
