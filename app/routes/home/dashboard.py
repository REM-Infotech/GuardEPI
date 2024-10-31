from flask import render_template, request, make_response, jsonify
from flask_login import login_required
from app import app
from app.models.EPI import RegistrosEPI, RegistroEntradas
from app.decorators import set_endpoint
from app.misc import format_currency_brl

from collections import Counter
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import extract


@app.route("/dashboard", methods=["GET"])
@login_required
@set_endpoint
def dashboard():
    """
    # Rota Dashboard

    ## Returns:
        title: titulo da página
        page: página a ser renderizada
        DataTables: JS Datatables para a página

    """
    now = datetime.now()
    current_day = now.day
    current_month = now.month

    dbase = RegistrosEPI.query.filter(
        extract("day", RegistrosEPI.data_solicitacao) == current_day,
        extract("month", RegistrosEPI.data_solicitacao) == current_month,
    ).all()

    dbase2 = RegistroEntradas.query.filter(
        extract("day", RegistroEntradas.data_entrada) == current_day,
        extract("month", RegistroEntradas.data_entrada) == current_month,
    ).all()

    total_saidas = len(dbase)
    total_entradas = len(dbase2)
    valor_total = 0

    valor_total = sum(map(lambda item: float(item.valor_total), dbase))
    valor_totalEntradas = sum(map(lambda item: float(item.valor_total), dbase2))

    database = RegistrosEPI.query.all()
    title = request.endpoint.capitalize()
    page = "pages/dashboard.html"
    DataTables = "js/DataTables/DashboardTable.js"

    resp = make_response(
        render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            DataTables=DataTables,
            total_saidas=total_saidas,
            valor_total=valor_total,
            format_currency_brl=format_currency_brl,
            valor_totalEntradas=valor_totalEntradas,
            total_entradas=total_entradas,
        )
    )

    return resp


@app.route("/saidasEquipamento", methods=["GET"])
def saidasEquipamento():

    current_date = datetime.now().date()

    # Calculando o início e o fim da semana atual, começando no domingo
    start_of_week = current_date - timedelta(days=current_date.weekday() + 1)  # Domingo
    end_of_week = start_of_week + timedelta(days=6)  # Sábado

    data = {
        "dias_semana": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
        "Saidas": [5, 10, 3, 25, 15],
        "media": 30,
    }

    # Consulta os dados do banco de dados filtrando pelo mês e ano atuais
    entregas = RegistrosEPI.query.filter(
        RegistrosEPI.data_solicitacao >= start_of_week,
        RegistrosEPI.data_solicitacao <= end_of_week,
    ).all()

    contar = Counter(entregas)

    return jsonify(data)


@app.route("/saidasFuncionario", methods=["GET"])
def saidasFuncionario():

    chart_data = {"labels": [], "values": [], "media": 0}

    # Obtendo o mês e ano atuais
    now = datetime.now()
    current_day = now.day
    current_month = now.month

    # Consulta os dados do banco de dados filtrando pelo mês e ano atuais
    entregas = RegistrosEPI.query.filter(
        extract("day", RegistrosEPI.data_solicitacao) == current_day,
        extract("month", RegistrosEPI.data_solicitacao) == current_month,
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

    return jsonify(chart_data)
