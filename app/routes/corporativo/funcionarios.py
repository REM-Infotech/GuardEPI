import traceback
from datetime import datetime
from pathlib import Path
from typing import Union

from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from quart import (
    Response,
    abort,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import FuncionarioForm
from app.models import Funcionarios
from app.routes.corporativo.setups import setup_form_funcionario

from . import corp

form_content = Union[str, FileStorage, int, float, datetime]


@corp.get("/funcionarios")
@login_required
@read_perm
async def funcionarios() -> Response:
    """
    Fetches all records from the Funcionarios table and renders the 'index.html' template with the data.
    This function queries all records from the Funcionarios table in the database and passes the data to the
    'index.html' template along with the page name 'funcionarios.html'. If an exception occurs during the process,
    it aborts the request with a 500 status code and includes the exception message in the response.
    Returns:
        Response: A Quart response object that renders the 'index.html' template with the fetched data.
    Raises:
        HTTPException: If an exception occurs, it aborts the request with a 500 status code and the exception message.
    """

    try:
        page = "funcionarios.html"
        database = Funcionarios.query.all()
        return await make_response(
            await render_template(
                "index.html",
                page=page,
                database=database,
            )
        )
    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@corp.get("/funcionarios_rest")
async def funcionarios_rest() -> Response:
    """
    Fetches all records from the Funcionarios table and renders the 'index.html' template with the data.
    This function queries all records from the Funcionarios table in the database and passes the data to the
    'index.html' template along with the page name 'funcionarios.html'. If an exception occurs during the process,
    it aborts the request with a 500 status code and includes the exception message in the response.
    Returns:
        Response: A Quart response object that renders the 'index.html' template with the fetched data.
    Raises:
        HTTPException: If an exception occurs, it aborts the request with a 500 status code and the exception message.
    """

    try:
        db: SQLAlchemy = current_app.extensions["sqlalchemy"]

        database = db.session.query(Funcionarios).all()

        return await make_response(
            jsonify(
                data=[
                    dict(
                        id=item.id,
                        nome=item.nome_funcionario,
                        matricula=item.codigo,
                        cargo=item.cargo,
                        departamento=item.departamento,
                    )
                    for item in database
                ]
            )
        )
    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@corp.route("/funcionarios/cadastro", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastro_funcionarios() -> Response:
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

    try:
        title = "Cadastro de Funcionário"
        page = "forms/funcionario_form.html"

        form = FuncionarioForm()

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

            item = Funcionarios(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                await flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            await flash("Funcionário cadastrado com sucesso!", "success")
            return await make_response(redirect(url_for("corp.funcionarios")))

        return await make_response(
            await render_template("index.html", title=title, page=page, form=form)
        )

    except Exception as e:
        app.logger.error("\n".join(traceback.format_exception(e)))
        abort(500)


@corp.route("/funcionarios/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
async def editar_funcionarios(id: int) -> Response:
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

    try:
        title = "Editar Funcionário"
        page = "forms/funcionario_form.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        funcionario = db.session.query(Funcionarios).filter_by(id=id).first()
        url_image = ""

        form_data = {}
        form_data, url_image = await setup_form_funcionario(funcionario)
        form = FuncionarioForm(**form_data)
        if form.validate_on_submit():
            form_data: dict[str, form_content] = list(
                filter(
                    lambda x: x[1] and x[0] != "csrf_token" or x[0] != "submit",
                    list(form.data.items()),
                )
            )
            for key, value in form_data:
                if isinstance(value, FileStorage):
                    filename = secure_filename(value.filename)
                    path_file = Path(app.config.get("TEMP_PATH")).joinpath(filename)
                    value.save(str(path_file))
                    setattr(funcionario, "filename", filename)
                    setattr(funcionario, "blob_doc", value.stream.read())
                    continue

                setattr(funcionario, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                await flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html",
                        title=title,
                        page=page,
                        form=form,
                        url_image=url_image,
                    )
                )
            except Exception as e:
                app.logger.error("\n".join(traceback.format_exception(e)))
                return await make_response(
                    await render_template(
                        "index.html",
                        title=title,
                        page=page,
                        form=form,
                        url_image=url_image,
                    )
                )
            await flash("Edições Salvas con sucesso!", "success")
            return await make_response(redirect(url_for("corp.funcionarios")))

        return await make_response(
            await render_template(
                "index.html",
                title=title,
                page=page,
                form=form,
                url_image=url_image,
            )
        )

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@corp.post("/funcionarios/deletar/<int:id>")
@login_required
@delete_perm
async def deletar_funcionarios(id: int) -> Response:
    """
    Deletes an employee record from the database based on the provided ID.
    Args:
        id (int): The ID of the employee to be deleted.
    Returns:
        Response: A rendered template with a success message indicating that the information was successfully deleted.
    """

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        func = db.session.query(Funcionarios).filter_by(id=id).first()

        db.session.delete(func)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(await render_template(template, message=message))

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(await render_template(template, message=message))
