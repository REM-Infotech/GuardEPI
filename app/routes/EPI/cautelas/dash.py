from pathlib import Path
from uuid import uuid4

from flask import current_app as app
from flask import render_template, request, send_from_directory, session, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.misc import format_currency_brl
from app.models import RegistroSaidas, RegistrosEPI

from .. import estoque_bp


@estoque_bp.route("/registro_saidas", methods=["GET"])
@login_required
def registro_saidas():

    page = "registro_saidas.html"
    database = RegistroSaidas.query.all()
    title = request.endpoint.split(".")[1].capitalize().replace("_", " ")

    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        format_currency_brl=format_currency_brl,
    )


@estoque_bp.route("/cautelas", methods=["GET"])
@login_required
def cautelas(to_show: str = None):

    url = None
    to_show = request.args.get("to_show", to_show)
    if to_show:

        url = url_for("estoque.cautela_pdf", uuid_pasta=to_show)

    page = "cautelas.html"
    database = RegistrosEPI.query.all()
    title = request.endpoint.split(".")[1].capitalize()

    session["itens_lista_cautela"] = []
    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        url=url,
    )


@estoque_bp.get("/cautela_pdf/<uuid_pasta>")
def cautela_pdf(uuid_pasta: str):
    """
    Route to serve an image file.
    This route handles GET requests to serve an image file from a specified directory.
    The filename is provided as a URL parameter.
    Args:
        filename (str): The name of the image file to be served.
    Returns:
        Response: A Flask response object that sends the requested image file from the directory specified in the app configuration.
    """
    path_cautela = Path(app.config["DOCS_PATH"]).joinpath(uuid_pasta)

    if path_cautela.exists():
        filename = next(path_cautela.glob("*.pdf")).name

    if not path_cautela.exists():

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        query_file = db.session.query(RegistrosEPI).filter_by(id=uuid_pasta).first()

        filename = query_file.filename
        path_cautela = Path(app.config["DOCS_PATH"]).joinpath(str(uuid4()))
        path_cautela.mkdir(exist_ok=True)

        with path_cautela.joinpath(filename).open("wb") as file:
            file.write(query_file.blob_doc)

    return send_from_directory(path_cautela, filename)
