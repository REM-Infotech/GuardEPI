from datetime import datetime
from pathlib import Path
from typing import Union

from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.forms import CadastroEmpresa
from app.models import Empresa

from . import corp

form_content = Union[str, FileStorage, int, float, datetime]


@corp.route("/Empresas", methods=["GET"])
@login_required
def Empresas():
    """
    Handles the route for displaying the 'Empresas' page.
    This function creates an instance of the CadastroEmpresa form and retrieves all records from the Empresa database.
    It then renders the 'index.html' template with the 'empresas.html' page, the form, and the database records.
    Returns:
        Response: The rendered template for the 'Empresas' page.
    Raises:
        HTTPException: If an error occurs during the process, a 500 Internal Server Error is raised with the error description.
    """

    try:

        database = Empresa.query.all()

        page = "empresas.html"
        return render_template(
            "index.html",
            page=page,
            database=database,
        )

    except Exception as e:
        abort(500, description=str(e))


@corp.route("/Empresas/cadastro", methods=["GET", "POST"])
@login_required
def cadastro_empresas():
    """
    Handles the registration of companies.
    This function processes the form data submitted for company registration,
    validates the form, and saves the data to the database. It also handles
    file uploads and converts specific form fields as needed.
    Returns:
        Response: A redirect response to the 'corp.Empresas"))' page if the form
        is successfully validated and data is committed to the database.
        Otherwise, it renders the 'index.html' template with the form.
    Raises:
        Exception: Any exceptions raised during database operations or file handling
        will propagate up to the caller.
    """

    endpoint = "Empresas"
    act = "Cadastro"

    form = CadastroEmpresa()

    if form.validate_on_submit():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        to_add = {}

        form_data: dict[str, form_content] = list(form.data.items())
        for key, value in form_data:
            if key == "csrf_token":
                continue

            if key == "submit":
                continue

            if key == "valor_unitario":
                value = float(
                    value.replace(",", ".").replace("R$", "").replace(" ", "")
                )

            if isinstance(value, FileStorage):
                filename = secure_filename(value.filename)
                path_file = Path(app.config.get("TEMP_PATH")).joinpath(filename)
                value.save(str(path_file))
                with path_file.open("rb") as file:
                    to_add.update({"blob_doc": file.read()})

                to_add.update({"filename": filename})
                continue

            to_add.update({key: value})

        emp = Empresa(**to_add)
        db.session.add(emp)
        db.session.commit()

        flash("emp cadastrado com sucesso!", "success")
        return redirect(url_for("corp.Empresas"))

    page = "forms/empresa_form.html"
    return render_template(
        "index.html", act=act, endpoint=endpoint, page=page, form=form
    )


@corp.route("/Empresas/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_empresas(id: int):
    """
    Edit an existing company record in the database.
    This function handles both GET and POST requests to edit a company's details.
    On a GET request, it retrieves the company's current data and pre-fills a form.
    On a POST request, it validates the form data and updates the company's record in the database.
    Args:
        id (int): The ID of the company to be edited.
    Returns:
        Response: A rendered template for the company edit form on GET request.
                  A redirect to the equipment page on successful form submission.
    """

    endpoint = "Empresas"
    act = "Editar"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    emp = db.session.query(Empresa).filter_by(id=id).first()

    form_data = {}

    form = CadastroEmpresa()

    if request.method == "GET":

        url_image = ""
        emp_data = emp.__dict__

        items_emp_data = list(emp_data.items())

        for key, value in items_emp_data:

            if key == "_sa_instance_state" or key == "id" or key == "filename":

                continue

            if key == "blob_doc":

                img_path = (
                    Path(app.config.get("TEMP_PATH"))
                    .joinpath("IMG")
                    .joinpath(emp_data.get("filename"))
                )
                with img_path.open("wb") as file:
                    file.write(value)

                with img_path.open("rb") as file:
                    form_data.update(
                        {
                            "filename": FileStorage(
                                filename=secure_filename(emp.filename),
                                stream=file.read(),
                            )
                        }
                    )

                    url_image = url_for(
                        "serve.serve_img", filename=emp.filename, _external=True
                    )

            form_data.update({key: value})

        form = CadastroEmpresa(**form_data)

    if form.validate_on_submit():

        to_add = {}

        form_data: dict[str, form_content] = list(form.data.items())
        for key, value in form_data:

            if value:
                if key == "csrf_token":
                    continue

                if key == "submit":
                    continue

                if isinstance(value, FileStorage):
                    filename = secure_filename(value.filename)
                    path_file = Path(app.config.get("TEMP_PATH")).joinpath(filename)
                    value.save(str(path_file))
                    with path_file.open("rb") as file:
                        to_add.update({"blob_doc": file.read()})

                    to_add.update({"filename": filename})
                    continue

                setattr(emp, key, value)

        db.session.commit()

        flash("Edições Salvas con sucesso!", "success")
        return redirect(url_for("corp.Empresas"))

    page = "forms/empresa_form.html"
    return render_template(
        "index.html",
        act=act,
        endpoint=endpoint,
        page=page,
        form=form,
        url_image=url_image,
    )


@corp.route("/Empresas/deletar/<int:id>")
@login_required
def deletar_empresas(id: int):
    """
    Deletes a company record from the database based on the provided ID.
    Args:
        id (int): The ID of the company to be deleted.
    Returns:
        Response: A rendered HTML template with a success message.
    Raises:
        sqlalchemy.orm.exc.NoResultFound: If no company with the given ID is found.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    emp = db.session.query(Empresa).filter_by(id=id).first()

    db.session.delete(emp)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
