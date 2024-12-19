from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors

from app.forms import CadastroMarcas
from app.models import Marcas

from . import epi


@epi.route("/marcas", methods=["GET"])
@login_required
def marcas():
    """
    Fetches all records from the Marcas table and renders the 'index.html' template with the 'marcas.html' page and the retrieved database records.
    Returns:
        str: Rendered HTML template with the specified page and database records.
    """

    page = "marcas.html"
    database = Marcas.query.all()
    return render_template("index.html", page=page, database=database)


@epi.route("/marca/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_marca():
    """
    Handles the registration of a new brand (marca).
    This function processes the form submission for registering a new brand.
    It validates the form data, creates a new Marcas instance, adds it to the
    database, and commits the transaction. If the form submission is successful,
    it flashes a success message and redirects to the 'epi.marcas' endpoint.
    Otherwise, it renders the form for the user to fill out.
    Returns:
        Response: A redirect response to the 'epi.marcas' endpoint if the form
        is successfully submitted and processed. Otherwise, it returns a rendered
        template with the form for the user to fill out.
    """

    endpoint = "marca"
    act = "Cadastro"
    form = CadastroMarcas()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        classe = Marcas(**to_add)
        db.session.add(classe)
        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("Marca cadastrada com sucesso!", "success")
        return redirect(url_for("epi.marcas"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/marca/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_marca(id):
    """
    Edit a brand (marca) based on the given ID.
    This function handles the editing of a brand by retrieving the brand's
    information from the database, populating a form with the current data,
    and updating the brand's information if the form is submitted and validated.
    Args:
        id (int): The ID of the brand to be edited.
    Returns:
        Response: If the request method is GET, it returns the rendered template
        with the form populated with the brand's current data. If the form is
        submitted and validated, it updates the brand's information in the
        database, flashes a success message, and redirects to the brand listing
        page.
    """

    endpoint = "marca"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroMarcas()

    classe = db.session.query(Marcas).filter(Marcas.id == id).first()

    if request.method == "GET":
        form = CadastroMarcas(**classe.__dict__)

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

        flash("Marca editada com sucesso!", "success")
        return redirect(url_for("epi.marcas"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/marcas/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_marca(id: int):
    """
    Deletes a brand entry from the database based on the provided ID.
    Args:
        id (int): The ID of the brand to be deleted.
    Returns:
        Response: A rendered template with a success message indicating that the information has been deleted.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    classe = db.session.query(Marcas).filter(Marcas.id == id).first()

    db.session.delete(classe)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
