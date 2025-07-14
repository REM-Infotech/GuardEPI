from flask_sqlalchemy import SQLAlchemy
from quart import (
    current_app,
    make_response,
    render_template,
    request,
    session,
    url_for,
)
from quart_auth import login_required

from app.decorators import read_perm
from app.misc import format_currency_brl
from app.models import RegistroSaidas, RegistrosEPI
from app.routes.epi import estoque_bp
from app.routes.epi.cautelas.interface import RegistrosEPIClass

from . import forms_routes, serving

__all__ = ["forms_routes", "serving"]


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


@estoque_bp.route("/cautelas", methods=["GET"])
@login_required
@read_perm
async def cautelas(to_show: str = None) -> str:
    url = None
    title = "Liberações de EPI's"
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]
    to_show = request.args.get("to_show", to_show)
    if to_show:
        url = url_for("estoque.cautela_pdf", uuid_pasta=to_show)

    page = "cautelas.html"
    data = db.session.query(RegistrosEPI).all()

    if len(data) > 0:
        data = list(filter(lambda x: not x.cautela_cancelada, data))

    database = [RegistrosEPIClass(**dict(list(item.__dict__.items()))) for item in data]

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
