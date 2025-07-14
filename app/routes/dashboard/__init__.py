import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pandas as pd
import pytz
from flask_sqlalchemy import SQLAlchemy
from quart import (
    Blueprint,
    Response,
    abort,
    current_app,
    jsonify,
    make_response,
    render_template,
)
from quart import current_app as app
from quart_auth import login_required
from sqlalchemy import extract

from app.models.EPI.cautelas import RegistrosEPIRedis

from ...misc import format_currency_brl
from ...models import RegistroEntradas, RegistroSaidas, RegistrosEPI

template_folder = Path(__file__).parent.resolve().joinpath("templates")
dash = Blueprint("dash", __name__, template_folder=template_folder)


async def get_registro_saidas() -> List[RegistrosEPI]:
    # First try to get from Redis

    pkeys = []
    cached_registros: list[dict[str, str]] = []
    for index, item in enumerate(RegistrosEPIRedis.all_pks()):
        pkeys.append(item)

    for pkey in pkeys:
        cached_registros.append(RegistrosEPIRedis.get(pkey).model_dump())

    if cached_registros:
        return [
            RegistrosEPI(
                **{
                    k: v
                    for k, v in list(registro.items())
                    if k != "pk" and k != "blob_doc" and k
                }
            )
            for registro in cached_registros
        ]

    # If not in Redis, get from database
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]
    db.get_engine()
    database = db.session.query(RegistrosEPI).all()

    if len(database) > 0:
        database = database[:50]

    def decode_blob(b: bytes) -> str:
        if b == b"":
            return b
        decoded = b.decode(encoding="ISO-8859-1")
        return decoded

    # Convert to Redis models and cache them
    registros_epi = [
        RegistrosEPIRedis(
            **{
                "id": item.id,
                "nome_epis": str(item.nome_epis),
                "valor_total": item.valor_total,
                "funcionario": item.funcionario,
                "data_solicitacao": item.data_solicitacao,
                "filename": item.filename,
                "blob_doc": decode_blob(item.blob_doc if item.blob_doc else b""),
            }
        )
        for item in database
    ]

    for item in registros_epi:
        RegistrosEPIRedis.db().expire(item.key(), timedelta(seconds=600))

    # Cache in Redis
    RegistrosEPIRedis.add(registros_epi)

    return database


@dash.route("/dashboard", methods=["GET"])
@login_required
async def dashboard() -> Response:
    """
    Renders the dashboard page with various statistics and data for the current month.
    This function retrieves data from the database for the current month, including
    total entries, total exits, and their respective values. It then renders the
    'index.html' template with the retrieved data.
    Returns:
        Response: A Quart response object containing the rendered template.
    Raises:
        HTTPException: If an error occurs during data retrieval or template rendering,
                       a 500 HTTP error is raised with the error description.
    """

    try:
        db: SQLAlchemy = current_app.extensions["sqlalchemy"]
        now = datetime.now(pytz.timezone("Etc/GMT+4"))
        current_month = now.month
        month = str(now.month)
        year = str(now.year)

        if len(month) == 1:
            month = f"0{month}"

        data = await get_registro_saidas()

        valor_total = 0
        valor_totalEntradas = 0
        total_entradas = 0
        total_saidas = 0

        dbase = RegistroSaidas.query.filter(
            extract("month", RegistroSaidas.data_saida) == current_month
        ).all()

        dbase2 = RegistroEntradas.query.filter(
            extract("month", RegistroEntradas.data_entrada) == current_month
        ).all()

        for item in dbase2:
            total_entradas += int(item.qtd_entrada)
            valor_totalEntradas += float(item.valor_total)

        for item in dbase:
            total_saidas += int(item.qtd_saida)
            valor_total += float(item.valor_total) * item.qtd_saida

        # valor_total = sum(map(lambda item: float(item.valor_total), dbase))
        # valor_totalEntradas = sum(map(lambda item: float(item.valor_total), dbase2))

        if not data:
            data = db.session.query(RegistrosEPI).all()[:50]

        database = data

        title = "Dashboard"
        page = "dashboard.html"

        # today = datetime.now().strftime("%d/%m/%Y")

        return await make_response(
            await render_template(
                "index.html",
                page=page,
                title=title,
                database=database,
                total_saidas=total_saidas,
                valor_total=valor_total,
                format_currency_brl=format_currency_brl,
                valor_totalEntradas=valor_totalEntradas,
                total_entradas=total_entradas,
                month=month,
                year=year,
            )
        )

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@dash.route("/saidasEquipamento", methods=["GET"])
@login_required
async def saidasEquipamento() -> Response:
    """
    Retrieves equipment output data for the current month and returns it in JSON format.
    This function queries the database for equipment output records for the current month,
    processes the data to calculate the total values and average, and returns the data
    formatted for charting.
    Returns:
        Response: A Quart JSON response containing the chart data with the following structure:
            {
                "labels": [list of equipment names],
                "values": [list of total values for each equipment],
                "media": calculated average value
    """

    try:
        chart_data = {"labels": [], "values": [], "media": 0}

        # Obtendo o mês e ano atuais
        now = datetime.now()
        # current_day = now.day
        current_month = now.month

        # Consulta os dados do banco de dados filtrando pelo mês e ano atuais
        entregas = RegistroSaidas.query.filter(
            extract("month", RegistroSaidas.data_saida) == current_month
        ).all()

        if entregas:
            data = {
                "Equipamento": [entrega.nome_epi for entrega in entregas],
                "Valor": [entrega.valor_total for entrega in entregas],
            }

            df = pd.DataFrame(data)

            # Agrupando por 'Equipamento' e somando os valores
            df_grouped = df.groupby("Equipamento").sum().reset_index()

            media_old = int(sorted(df_grouped["Valor"].tolist())[-1])

            # Calcula a diferença
            media = media_old + ((media_old // 100 + 1) * 100 - media_old)

            # Convertendo os dados para JSON
            chart_data = {
                "labels": df_grouped["Equipamento"].tolist(),
                "values": df_grouped["Valor"].tolist(),
                "media": media,
            }
        return await make_response(jsonify(chart_data))

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@dash.route("/saidasFuncionario", methods=["GET"])
@login_required
async def saidasFuncionario() -> Response:
    """
    Retrieves and processes employee data for the current month to generate chart data.
    This function queries the database for records of employee deliveries (RegistrosEPI)
    filtered by the current month. It then constructs a DataFrame from the retrieved data,
    groups the data by employee, and calculates the total value for each employee. Additionally,
    it calculates a media value based on the highest total value.
    Returns:
        Response: A JSON response containing the chart data with labels (employee names),
                  values (total values), and media (calculated media value).
    """

    try:
        chart_data = {"labels": [], "values": [], "media": 0}

        # Obtendo o mês e ano atuais
        now = datetime.now()
        # current_day = now.day
        current_month = now.month

        # Consulta os dados do banco de dados filtrando pelo mês e ano atuais
        entregas = RegistrosEPI.query.filter(
            extract("month", RegistrosEPI.data_solicitacao) == current_month
        ).all()

        if entregas:
            # Construa o DataFrame
            data = {
                "Funcionario": [entrega.funcionario for entrega in entregas],
                "Valor": [entrega.valor_total for entrega in entregas],
            }
            df = pd.DataFrame(data)

            # Agrupando por 'Funcionario' e somando os valores
            df_grouped = df.groupby("Funcionario").sum().reset_index()

            media_old = int(sorted(df_grouped["Valor"].tolist())[-1])
            # Calcula a diferença
            media = media_old + ((media_old // 100 + 1) * 100 - media_old)

            # Convertendo os dados para JSON
            chart_data = {
                "labels": df_grouped["Funcionario"].tolist(),
                "values": df_grouped["Valor"].tolist(),
                "media": media,
            }

        return await make_response(jsonify(chart_data))

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


# @dash.route("/test_celery", methods=["GET"])
# def test_celery():
#     result = send_email.delay(15, 15)

#     return jsonify({"result_id": result.id}), 200


# @dash.route("/result/<id>", methods=["GET"])
# def task_result(id: str) -> dict[str, object]:
#     result = AsyncResult(id)
#     return {
#         "ready": result.ready(),
#         "successful": result.successful(),
#         "value": result.result if result.ready() else None,
#     }
