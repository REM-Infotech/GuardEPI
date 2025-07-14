from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from quart import (
    Response,
    abort,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required
from werkzeug.datastructures import MultiDict

from app.decorators import create_perm, read_perm
from app.forms.epi import CancelarCautelaForm, FormEnvioCautelaAssinada
from app.misc import format_currency_brl
from app.models import CautelaAssinada, RegistroSaidas, RegistrosEPI
from app.routes.epi.cautelas.actions import add_cautela_assinada

from .. import estoque_bp


class RegistrosEPIClass:
    id: int = None
    nome_epis: str = None
    valor_total: str = None
    funcionario: str = None
    data_solicitacao: datetime = None
    filename: str = None
    blob_doc: bytes = None
    documentos_assinados: list = None

    def __init__(self, **kwargs):
        for item in dir(RegistrosEPIClass):
            if item.startswith("_"):
                continue

            to_add = kwargs.get(item)
            if to_add:
                if item == "documentos_assinados":
                    if len(to_add) > 0:
                        val: CautelaAssinada = to_add[-1]
                        setattr(self, item, val)
                        continue

                    elif len(to_add) == 0:
                        setattr(self, item, None)
                        continue

                setattr(self, item, to_add)


@estoque_bp.route("/envio_cautela_assinada/<int:id_cautela>", methods=["GET", "POST"])
@login_required
@create_perm
async def envio_cautela_assinada(id_cautela: int) -> Response:
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]

    query = db.session.query(RegistrosEPI).filter_by(id=id_cautela).first()

    list_items_data = [
        ("nome_funcionario", query.funcionario),
        ("nome_cautela", query.filename),
    ]

    if request.method == "POST":
        fm = await request.form
        files = await request.files
        if not fm.get("confirm_form"):
            await flash("É necessário aceitar os termos do formulário")
            return await make_response(redirect(url_for("estoque.cautelas")))

        files_data = dict(list(files.items()))
        form_data = dict(list(fm.items()))

        list_items_data.extend(list(form_data.items()))
        list_items_data.extend(list(files_data.items()))

    data = MultiDict(list_items_data)

    form = FormEnvioCautelaAssinada(formdata=data)
    url_action = request.full_path

    if form.validate_on_submit():
        await add_cautela_assinada(form, query, db)

        await flash("Cautela assinada salva com sucesso!", "success")
        return await make_response(redirect(url_for("estoque.cautelas")))

    if request.method == "GET":
        return await make_response(
            await render_template(
                "forms/envio_assinado.html",
                form=form,
                url_action=url_action,
            )
        )

    return await make_response(redirect(url_for("estoque.cautelas")))


@estoque_bp.route("/cancelar_cautela/<int:id_cautela>", methods=["GET", "POST"])
@login_required
@create_perm
async def cancelar_cautela(id_cautela: int) -> Response:
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]
    query = db.session.query(RegistrosEPI).filter_by(id=id_cautela).first()

    list_items_data = [
        ("nome_funcionario", query.funcionario),
        ("nome_cautela", query.filename),
    ]

    if request.method == "POST":
        fm = await request.form

        if not fm.get("confirm_form"):
            await flash("É necessário aceitar os termos do formulário")
            return await make_response(redirect(url_for("estoque.cautelas")))

        list_items_data.extend(list(dict(list(fm.items())).items()))

    data = MultiDict(list_items_data)

    form = CancelarCautelaForm(formdata=data)
    url_action = request.full_path

    if form.validate_on_submit():
        await flash("Cautela cancelada com sucesso!", "success")

    if request.method == "GET":
        return await make_response(
            await render_template(
                "forms/cancelar_cautela.html",
                form=form,
                url_action=url_action,
            )
        )

    return await make_response(redirect(url_for("estoque.cautelas")))


@estoque_bp.route("/registro_saidas", methods=["GET"])
@login_required
@read_perm
async def registro_saidas() -> str:
    page = "registro_saidas.html"
    database = RegistroSaidas.query.all()
    title = "Registro Saídas"

    return await make_response(
        await render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            format_currency_brl=format_currency_brl,
        )
    )


# @estoque_bp.route("/registro_saidas_rest", methods=["GET"])
# async def registro_saidas_rest() -> Response:
#     return await make_response(
#         jsonify(
#             data=[
#                 dict(
#                     id=item.id,
#                     funcionario=item.funcionario,
#                     epis_entregues=item.nome_epis,
#                     data_entregue=item.data_solicitacao.strftime("%d/%m/%Y"),
#                     documento_assinado=item.filename,
#                 )
#                 for item in await get_registro_saidas()
#             ]
#         )
#     )


@estoque_bp.route("/cautelas", methods=["GET"])
@login_required
@read_perm
async def cautelas(to_show: str = None) -> str:
    url = None
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]
    to_show = request.args.get("to_show", to_show)
    if to_show:
        url = url_for("estoque.cautela_pdf", uuid_pasta=to_show)

    page = "cautelas.html"
    data = db.session.query(RegistrosEPI).all()
    title = "Liberações de EPI's"

    database = []

    for item in data:
        formated_data = RegistrosEPIClass(**dict(list(item.__dict__.items())))
        database.append(formated_data)

    session["itens_lista_cautela"] = []
    return await make_response(
        await render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            url=url,
        )
    )


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
