from pathlib import Path
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from quart import Response, abort, make_response, send_from_directory
from quart import current_app as app

from app.decorators import read_perm
from app.models.EPI.cautelas import CautelaAssinada, RegistrosEPI
from app.routes.epi import estoque_bp


@estoque_bp.get("/cautela_pdf/<uuid_pasta>")
@read_perm
async def cautela_pdf(uuid_pasta: str) -> Response:
    """
    Route to serve an image file.
    This route handles GET requests to serve an image file from a specified directory.
    The filename is provided as a URL parameter.
    Args:
        filename (str): The name of the image file to be served.
    Returns:
        Response: A Quart response object that sends the requested image file from the directory specified in the app configuration.
    """

    path_cautela = ""
    filename = ""

    path_cautela = Path(app.config["DOCS_PATH"]).joinpath(uuid_pasta)

    if path_cautela.exists():
        filename = next(path_cautela.glob("*.pdf")).name

    elif not path_cautela.exists():
        try:
            uuid_pasta = int(uuid_pasta)

        except ValueError:
            uuid_pasta = uuid_pasta

        if isinstance(uuid_pasta, int):
            db: SQLAlchemy = app.extensions["sqlalchemy"]
            query_file = db.session.query(RegistrosEPI).filter_by(id=uuid_pasta).first()

            filename = query_file.filename
            path_cautela = Path(app.config["DOCS_PATH"]).joinpath(str(uuid4()))
            path_cautela.mkdir(exist_ok=True)

            with path_cautela.joinpath(filename).open("wb") as file:
                file.write(query_file.blob_doc)

        else:
            abort(404, description="Arquivo não encontrado")

    return await make_response(await send_from_directory(path_cautela, filename))


@estoque_bp.get("/cautela_assinada_pdf/<uuid_pasta>")
@read_perm
async def cautela_assinada_pdf(uuid_pasta: str) -> Response:
    """
    Route to serve an image file.
    This route handles GET requests to serve an image file from a specified directory.
    The filename is provided as a URL parameter.
    Args:
        filename (str): The name of the image file to be served.
    Returns:
        Response: A Quart response object that sends the requested image file from the directory specified in the app configuration.
    """

    path_cautela = ""
    filename = ""

    path_cautela = Path(app.config["DOCS_PATH"]).joinpath(uuid_pasta)

    if path_cautela.exists():
        filename = next(path_cautela.glob("*.pdf")).name

    elif not path_cautela.exists():
        try:
            uuid_pasta = int(uuid_pasta)

        except ValueError:
            uuid_pasta = uuid_pasta

        if isinstance(uuid_pasta, int):
            db: SQLAlchemy = app.extensions["sqlalchemy"]
            query_file = (
                db.session.query(CautelaAssinada).filter_by(id=uuid_pasta).first()
            )

            filename = query_file.filename
            path_cautela = Path(app.config["DOCS_PATH"]).joinpath(str(uuid4()))
            path_cautela.mkdir(exist_ok=True)

            with path_cautela.joinpath(filename).open("wb") as file:
                file.write(query_file.blob_doc)

        else:
            abort(404, description="Arquivo não encontrado")

    return await make_response(await send_from_directory(path_cautela, filename))
