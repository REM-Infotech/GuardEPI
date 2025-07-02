import traceback
from datetime import datetime
from pathlib import Path
from typing import Union

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
from quart_auth import login_required
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

# pragma: no cover
from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import FormProduto
from app.misc import format_currency_brl
from app.models import ProdutoEPI

from . import epi

form_content = Union[str, FileStorage, int, float, datetime]


@epi.route("/equipamentos")
@login_required
@read_perm
async def Equipamentos() -> Response:
    """
    Renders the 'equipamentos' page with the necessary context.
    This function retrieves all entries from the ProdutoEPI database, constructs
    the page title from the request endpoint, and sets the URL for an image icon.
    It then renders the 'index.html' template with the provided context.
    Returns:
        A rendered HTML template for the 'equipamentos' page.
    """
    page = "equipamentos.html"
    title = "Equipamentos"
    database = ProdutoEPI.query.all()
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return await make_response(
        await render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            format_currency_brl=format_currency_brl,
            url_image=url,
        )
    )


@epi.route("/equipamentos/cadastro", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastro_equipamento() -> Response:
    try:
        """
        Handles the registration of new EPI (Personal Protective Equipment).
        This function processes the form data submitted for registering a new EPI.
        It validates the form, processes the data, and saves it to the database.
        If the form submission is successful, it flashes a success message and redirects
        to the Equipamentos page. Otherwise, it renders the form page again.
        Returns:
            Response: A redirect response to the Equipamentos page if the form is successfully submitted,
                    or a rendered template of the form page if the form is not submitted or is invalid.
        """
        title = "Cadastro de Equipamento"
        page = "forms/equipamento_form.html"

        form = FormProduto()

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

            item = ProdutoEPI(**to_add)
            db.session.add(item)
            try:
                db.session.commit()

            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            flash("EPI cadastrado com sucesso!", "success")
            return await make_response(redirect(url_for("epi.Equipamentos")))

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/equipamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
async def editar_equipamento(id: int) -> Response:
    try:
        """
        Edit an existing EPI (Equipamento de Proteção Individual) record in the database.
        This function handles both GET and POST requests. On a GET request, it retrieves the EPI data from the database,
        populates a form with the data, and renders the form for editing. On a POST request, it validates the form data,
        updates the EPI record in the database, and saves any uploaded files.
        Args:
            id (int): The ID of the EPI record to be edited.
        Returns:
            Response: A rendered template for the EPI form on GET request, or a redirect to the EPI list page on successful form submission.
        """

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        epi = db.session.query(ProdutoEPI).filter_by(id=id).first()

        form_data = {}

        title = "Editar Equipamento"
        page = "forms/equipamento_form.html"

        url_image = ""
        epi_data = epi.__dict__
        items_epi_data = list(epi_data.items())

        for key, value in items_epi_data:
            if key == "_sa_instance_state" or key == "id" or key == "filename":
                continue

            if key == "blob_doc":
                if epi_data.get("filename"):
                    img_path = (
                        Path(app.config.get("TEMP_PATH"))
                        .joinpath("IMG")
                        .joinpath(epi_data.get("filename"))
                    )
                    with img_path.open("wb") as file:
                        file.write(value)

                    with img_path.open("rb") as file:
                        form_data.update(
                            {
                                "filename": FileStorage(
                                    filename=secure_filename(epi.filename),
                                    stream=file.read(),
                                )
                            }
                        )

                        url_image = url_for(
                            "serve.serve_img", filename=epi.filename, _external=True
                        )

            if key == "valor_unitario":
                value = format_currency_brl(value).replace("\\xa", "")

            form_data.update({key: value})

        form = FormProduto(**form_data)

        if form.validate_on_submit():
            to_add = {}

            form_data: dict[str, form_content] = list(form.data.items())
            for key, value in form_data:
                if value:
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

                    setattr(epi, key, value)

            try:
                db.session.commit()

            except errors.UniqueViolation:
                flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html",
                        title=title,
                        page=page,
                        form=form,
                        url_image=url_image,
                    )
                )

            flash("Edições Salvas con sucesso!", "success")
            return await make_response(redirect(url_for("epi.Equipamentos")))

        if form.errors:
            pass

        return await make_response(
            await render_template(
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


@epi.post("/equipamentos/deletar/<int:id>")
@login_required
@delete_perm
async def deletar_equipamento(id: int) -> Response:
    try:
        """
        Deletes an equipment record from the database based on the provided ID.
        Args:
            id (int): The ID of the equipment to be deleted.
        Returns:
            Response: Renders a template with a success message indicating that the information was deleted successfully.
        """

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        epi = db.session.query(ProdutoEPI).filter_by(id=id).first()

        db.session.delete(epi)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar"
        template = "includes/show.html"

    return await make_response(render_template(template, message=message))
