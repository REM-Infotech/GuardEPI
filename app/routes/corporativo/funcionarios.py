from datetime import datetime
from pathlib import Path
from typing import Union

from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.forms import CadastroFuncionario
from app.models import Funcionarios

from . import corp

form_content = Union[str, FileStorage, int, float, datetime]


@corp.get("/funcionarios")
@login_required
def funcionarios():
    """
    Fetches all records from the Funcionarios table and renders the 'index.html' template with the data.
    This function queries all records from the Funcionarios table in the database and passes the data to the
    'index.html' template along with the page name 'funcionarios.html'. If an exception occurs during the process,
    it aborts the request with a 500 status code and includes the exception message in the response.
    Returns:
        Response: A Flask response object that renders the 'index.html' template with the fetched data.
    Raises:
        HTTPException: If an exception occurs, it aborts the request with a 500 status code and the exception message.
    """

    try:

        page = "funcionarios.html"
        database = Funcionarios.query.all()
        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/funcionarios/cadastro", methods=["GET", "POST"])
@login_required
def cadastro_funcionarios():
    """
    Handles the registration of employees.
    This function processes the form data submitted for employee registration,
    validates the form, and saves the employee data to the database. It also
    handles file uploads and converts specific form fields as needed.
    Returns:
        Response: A redirect response to the employee list page if the form is
        successfully submitted and processed. Otherwise, it renders the form
        page with validation errors.
    Raises:
        ValueError: If there is an issue with form data conversion or file handling.
    """

    endpoint = "Funcionários"
    act = "Cadastro"

    form = CadastroFuncionario()

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

        func = Funcionarios(**to_add)
        db.session.add(func)
        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("func cadastrado com sucesso!", "success")
        return redirect(url_for("corp.funcionarios"))

    page = "forms/funcionario_form.html"
    return render_template(
        "index.html", act=act, endpoint=endpoint, page=page, form=form
    )


@corp.route("/funcionarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_funcionarios(id: int):
    """
    Edit an employee's information based on the given ID.
    This function handles both GET and POST requests. On a GET request, it retrieves the employee's data from the database,
    populates a form with this data, and renders the form for editing. On a POST request, it validates the form data, updates
    the employee's information in the database, and saves any uploaded files.
    Args:
        id (int): The ID of the employee to be edited.
    Returns:
        Response: A rendered template for the form on GET request, or a redirect to the employee list page on successful form submission.
    """

    endpoint = "Funcionários"
    act = "Editar"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    func = db.session.query(Funcionarios).filter_by(id=id).first()

    form_data = {}

    form = CadastroFuncionario()

    if request.method == "GET":

        url_image = ""
        emp_data = func.__dict__

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
                                filename=secure_filename(func.filename),
                                stream=file.read(),
                            )
                        }
                    )

                    url_image = url_for(
                        "serve.serve_img", filename=func.filename, _external=True
                    )

            form_data.update({key: value})

        form = CadastroFuncionario(**form_data)

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

                setattr(func, key, value)

        try:
            db.session.commit()
        except errors.UniqueViolation:
            abort(500, description="Item já cadastrado!")

        flash("Edições Salvas con sucesso!", "success")
        return redirect(url_for("corp.funcionarios"))

    page = "forms/funcionario_form.html"
    return render_template(
        "index.html",
        act=act,
        endpoint=endpoint,
        page=page,
        form=form,
        url_image=url_image,
    )


@corp.route("/funcionarios/deletar/<int:id>")
@login_required
def deletar_funcionarios(id: int):
    """
    Deletes an employee record from the database based on the provided ID.
    Args:
        id (int): The ID of the employee to be deleted.
    Returns:
        Response: A rendered template with a success message indicating that the information was successfully deleted.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    func = db.session.query(Funcionarios).filter_by(id=id).first()

    db.session.delete(func)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
