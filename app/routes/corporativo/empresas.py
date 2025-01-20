import traceback
from datetime import datetime
from pathlib import Path
from typing import Union

from flask import Response, abort
from flask import current_app as app
from flask import flash, make_response, redirect, render_template, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import EmpresaForm
from app.models import Empresa

from . import corp

form_content = Union[str, FileStorage, int, float, datetime]


@corp.route("/Empresas", methods=["GET"])
@login_required
@read_perm
def Empresas() -> Response:
    """
    Handles the route for displaying the 'Empresas' page.
    This function creates an instance of the EmpresaForm form and retrieves all records from the Empresa database.
    It then renders the 'index.html' template with the 'empresas.html' page, the form, and the database records.
    Returns:
        Response: The rendered template for the 'Empresas' page.
    Raises:
        HTTPException: If an error occurs during the process, a 500 Internal Server Error is raised with the error description.
    """

    try:

        database = Empresa.query.all()

        page = "empresas.html"
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


@corp.route("/Empresas/cadastro", methods=["GET", "POST"])
@login_required
@create_perm
def cadastro_empresas() -> Response:
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

    try:
        endpoint = "Empresas"
        act = "Cadastro"

        page = "forms/empresa_form.html"
        title = " ".join([act, endpoint])

        form = EmpresaForm()

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
            try:
                db.session.commit()
            except errors.UniqueViolation:

                flash("Item com informações duplicadas!")
                return make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("emp cadastrado com sucesso!", "success")
            return make_response(redirect(url_for("corp.Empresas")))

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.route("/Empresas/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
def editar_empresas(id: int) -> Response:
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

    try:

        endpoint = "Empresas"
        act = "Editar"

        page = "forms/empresa_form.html"
        title = " ".join([act, endpoint])

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        emp = db.session.query(Empresa).filter_by(id=id).first()

        form_data = {}

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

        form = EmpresaForm(**form_data)

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

            try:
                db.session.commit()
            except errors.UniqueViolation:

                flash("Item com informações duplicadas!")
                return make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            flash("Edições Salvas con sucesso!", "success")
            return make_response(redirect(url_for("corp.Empresas")))

        return make_response(
            render_template(
                "index.html",
                title=title,
                page=page,
                form=form,
                url_image=url_image,
            )
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@corp.post("/Empresas/deletar/<int:id>")
@login_required
@delete_perm
def deletar_empresas(id: int) -> Response:
    """
    Deletes a company record from the database based on the provided ID.
    Args:
        id (int): The ID of the company to be deleted.
    Returns:
        Response: A rendered HTML template with a success message.
    Raises:
        sqlalchemy.orm.exc.NoResultFound: If no company with the given ID is found.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        emp = db.session.query(Empresa).filter_by(id=id).first()

        db.session.delete(emp)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return make_response(render_template(template, message=message))

    except Exception:

        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return make_response(render_template(template, message=message))
