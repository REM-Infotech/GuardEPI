from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg import errors

from app.forms import CadastroModelos
from app.models import ModelosEPI

from . import epi


@epi.route("/modelos", methods=["GET"])
@login_required
def modelos():
    """
    Fetches all records from the ModelosEPI database and renders the 'index.html' template with the 'modelos.html' page and the database records.
    Returns:
        str: Rendered HTML template with the specified page and database records.
    """

    page = "modelos.html"
    database = ModelosEPI.query.all()
    return render_template("index.html", page=page, database=database)


@epi.route("/modelos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_modelos():
    """
    Handles the registration of new "modelos" (models) in the application.
    This function processes the form submission for registering new models.
    It validates the form data, extracts the relevant information, and adds
    a new entry to the database if the form is successfully validated.
    Returns:
        Response: A redirect to the "epi.modelos" endpoint if the form is successfully
                  submitted and processed, or renders the form template with the
                  appropriate context if the form is not submitted or is invalid.
    """

    endpoint = "modelos"
    act = "Cadastro"
    form = CadastroModelos()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        classe = ModelosEPI(**to_add)
        db.session.add(classe)

        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("modelos cadastrada com sucesso!", "success")
        return redirect(url_for("epi.modelos"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/modelos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_modelos(id: int):
    """
    Edit an existing 'ModelosEPI' entry in the database.
    This function handles the editing of a 'ModelosEPI' entry identified by the given ID.
    It supports both GET and POST requests. On a GET request, it populates the form with
    the existing data of the 'ModelosEPI' entry. On a POST request, it validates the form
    data, updates the 'ModelosEPI' entry, commits the changes to the database, and redirects
    to the 'modeloss' endpoint with a success message.
    Args:
        id (int): The ID of the 'ModelosEPI' entry to be edited.
    Returns:
        Response: Renders the 'index.html' template with the form for GET requests.
                  Redirects to the 'modeloss' endpoint with a success message for valid POST requests.
    """

    endpoint = "modelos"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroModelos()

    classe = db.session.query(ModelosEPI).filter(ModelosEPI.id == id).first()

    if request.method == "GET":
        form = CadastroModelos(**classe.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(classe, key, value)

        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("modelos editada com sucesso!", "success")
        return redirect(url_for("epi.modelos"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/modeloss/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_modelos(id: int):
    """
    Deletes a ModelosEPI record from the database based on the provided ID.
    Args:
        id (int): The ID of the ModelosEPI record to be deleted.
    Returns:
        Response: A rendered HTML template with a success message.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    classe = db.session.query(ModelosEPI).filter(ModelosEPI.id == id).first()

    db.session.delete(classe)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
