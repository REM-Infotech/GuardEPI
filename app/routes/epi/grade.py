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

from app.forms import FormGrade
from app.models import GradeEPI

from ...decorators import create_perm, delete_perm, read_perm, update_perm
from . import epi


@epi.route("/Grade")
@login_required
@read_perm
def Grade() -> Response:
    """
    Handles the request to display the grades page.
    This function queries the GradeEPI database for all entries and renders the
    'index.html' template with the retrieved data. If an exception occurs during
    the process, it aborts the request with a 500 status code and includes the
    exception message in the response.
    Returns:
        Response: A Quart response object that renders the 'index.html' template
        with the grades data.
    Raises:
        HTTPException: If an error occurs during the database query or template
        rendering, a 500 HTTPException is raised with the error description.
    """

    try:
        title = "Grades"
        page = "grade.html"

        database = GradeEPI.query.all()
        return await make_response(
            render_template(
                "index.html",
                page=page,
                title=title,
                database=database,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/Grade/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
def cadastrar_grade() -> Response:
    """
    Handles the creation and registration of a new GradeEPI entry.
    This function processes a form submission for creating a new GradeEPI.
    It validates the form data, constructs a new GradeEPI object, adds it to the database,
    and commits the transaction. If the form submission is successful, it flashes a success
    message and redirects to the grades page. If the form is not submitted or is invalid,
    it renders the form again.
    Returns:
        Response: A redirect response to the grades page if the form is successfully submitted
                  and processed, or a rendered template with the form if not.
    """

    try:
        endpoint = "Grade"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        form = FormGrade()
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if form.validate_on_submit():
            to_add = {}
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key.lower() == "csrf_token" or key.lower() == "submit":
                    continue

                to_add.update({key: value})

            item = GradeEPI(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Grade cadastrada com sucesso!", "success")
            return await make_response(redirect(url_for("epi.Grade")))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/Grade/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
def editar_grade(id) -> Response:
    """
    Edit a GradeEPI entry in the database.
    This function handles the editing of a GradeEPI entry identified by the given id.
    It supports both GET and POST requests. On a GET request, it populates the form with
    the existing data of the GradeEPI entry. On a POST request, it validates the form data,
    updates the GradeEPI entry, commits the changes to the database, and redirects to the
    grades list page with a success message.
    Args:
        id (int): The ID of the GradeEPI entry to be edited.
    Returns:
        Response: Renders the form template on GET request or redirects to the grades list
        page on successful form submission.
    """

    try:
        endpoint = "grade"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = FormGrade()

        grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

        if request.method == "GET":
            form = FormGrade(**grade.__dict__)

        if form.validate_on_submit():
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key != "csrf_token" or key != "submit" and value:
                    setattr(grade, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Grade editada com sucesso!", "success")
            return await make_response(redirect(url_for("epi.Grade")))

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.post("/grades/deletar/<int:id>")
@login_required
@delete_perm
def deletar_grade(id: int) -> Response:
    """
    Deletes a GradeEPI record from the database based on the provided ID.
    Args:
        id (int): The ID of the GradeEPI record to be deleted.
    Returns:
        Response: A rendered HTML template with a success message.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

        db.session.delete(grade)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
