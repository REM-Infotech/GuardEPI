from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from werkzeug.wrappers.response import Response

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import FormDepartamentos
from app.models import Departamento

from . import corp


@corp.route("/Departamentos")
@login_required
@read_perm
def Departamentos() -> str:
    """
    Handles the route for displaying the departments page.
    This function queries all departments from the database and renders the
    'index.html' template with the departments data. If an exception occurs
    during the process, it aborts the request with a 500 status code and
    includes the exception message in the response.
    Returns:
        Response: A Flask response object that renders the 'index.html' template
        with the departments data.
    Raises:
        HTTPException: If an exception occurs, a 500 HTTP status code is returned
        with the exception message.
    """

    try:

        page = "departamentos.html"
        database = Departamento.query.all()

        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/Departamentos/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
def cadastrar_departamentos() -> Response | str:
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

    endpoint = "Departamentos"
    act = "Cadastro"
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

        Departamentos = Departamento(**to_add)
        db.session.add(Departamentos)
        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("Departamentos cadastrada com sucesso!", "success")
        return redirect(url_for("corp.Departamentos"))

    return render_template(
        "index.html",
        page="form_base.html",
        form=form,
        endpoint=endpoint,
        act=act,
        title=" ".join([act.capitalize(), endpoint.capitalize()]),
    )


@corp.route("/Departamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
def editar_departamentos(id) -> Response | str:
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

    endpoint = "Departamentos"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = FormDepartamentos()

    Departamentos = db.session.query(Departamento).filter(Departamento.id == id).first()

    if request.method == "GET":
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
            abort(500, description="Item já cadastrado!")

        flash("Departamentos editada com sucesso!", "success")
        return redirect(url_for("corp.Departamentos"))

    return render_template(
        "index.html",
        page="form_base.html",
        form=form,
        endpoint=endpoint,
        act=act,
        title=" ".join([act.capitalize(), endpoint.capitalize()]),
    )


@corp.post("/Departamentoss/deletar/<int:id>")
@login_required
@delete_perm
def deletar_departamentos(id: int) -> str:
    """
    Deletes a department from the database based on the provided ID.
    Args:
        id (int): The ID of the department to be deleted.
    Returns:
        Response: Renders a template with a success message indicating that the information was successfully deleted.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    Departamentos = db.session.query(Departamento).filter(Departamento.id == id).first()

    db.session.delete(Departamentos)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
