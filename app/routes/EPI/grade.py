from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg import errors

from app.forms import CadastroGrade
from app.misc import format_currency_brl
from app.models import GradeEPI

from . import epi


@epi.route("/Grade")
@login_required
def Grade():
    """
    Handles the request to display the grades page.
    This function queries the GradeEPI database for all entries and renders the
    'index.html' template with the retrieved data. If an exception occurs during
    the process, it aborts the request with a 500 status code and includes the
    exception message in the response.
    Returns:
        Response: A Flask response object that renders the 'index.html' template
        with the grades data.
    Raises:
        HTTPException: If an error occurs during the database query or template
        rendering, a 500 HTTPException is raised with the error description.
    """

    try:
        title = "Grades"
        page = "grade.html"

        database = GradeEPI.query.all()
        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))


@epi.route("/Grade/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_grade():
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

    endpoint = "Grade"
    act = "Cadastro"
    form = CadastroGrade()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        grade = GradeEPI(**to_add)
        db.session.add(grade)
        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")
        flash("Grade cadastrada com sucesso!", "success")
        return redirect(url_for("epi.Grade"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/Grade/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_grade(id):
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

    endpoint = "grade"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroGrade()

    grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

    if request.method == "GET":
        form = CadastroGrade(**grade.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(grade, key, value)

        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("Grade editada com sucesso!", "success")
        return redirect(url_for("epi.Grade"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/grades/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_grade(id: int):
    """
    Deletes a GradeEPI record from the database based on the provided ID.
    Args:
        id (int): The ID of the GradeEPI record to be deleted.
    Returns:
        Response: A rendered HTML template with a success message.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

    db.session.delete(grade)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
