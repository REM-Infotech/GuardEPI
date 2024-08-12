from flask import render_template, request, make_response, jsonify
from flask_login import login_required
from app import app
from app.models.EPI import RegistrosEPI, RegistroEntradas
from app.decorators import set_endpoint
from app.misc import format_currency_brl

import pandas as pd
from datetime import datetime
from sqlalchemy import extract

@app.route("/dashboard", methods = ["GET"])
@login_required
@set_endpoint
def dashboard():
    
    """
    ## Rota Dashboard

    ### Returns:
        title: titulo da página
        page: página a ser renderizada
        DataTables: JS Datatables para a página
        
    """
    
    dbase = RegistrosEPI.query.all()
    dbase2 = RegistroEntradas.query.all()
    
    total_saidas = len(dbase)
    total_entradas = len(dbase2)
    valor_total = 0
    
    valor_total = sum(map(lambda item: float(item.valor_total), dbase))
    valor_totalEntradas = sum(map(lambda item: float(item.valor_total), dbase2))
    
    database = RegistrosEPI.query.all()
    title = request.endpoint.capitalize()
    page = "pages/dashboard.html"
    DataTables = 'js/DataTables/DashboardTable.js'
    
    resp = make_response(render_template("index.html", page = page, title = title, 
                           database = database, DataTables = DataTables, 
                           total_saidas = total_saidas, valor_total = valor_total,
                           format_currency_brl = format_currency_brl, 
                           valor_totalEntradas = valor_totalEntradas, total_entradas = total_entradas))
    

    return resp
    
@app.route("/saidasEquipamento", methods = ["GET"])
def saidasEquipamento():
    
    
    
    data = {"dias_semana": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
            "Saidas":  [5, 10 , 3, 25, 15],
            "media": 30}
    
    return jsonify(data)

@app.route("/saidasFuncionario", methods = ["GET"])
def saidasFuncionario():
    
    # Obtendo o mês e ano atuais
    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # Consulta os dados do banco de dados filtrando pelo mês e ano atuais
    entregas = RegistrosEPI.query.filter(
        extract('month', RegistrosEPI.data_solicitacao) == current_month,
        extract('year', RegistrosEPI.data_solicitacao) == current_year
    ).all()

    # Construa o DataFrame
    data = {
        'Funcionario': [entrega.funcionario for entrega in entregas],
        'Valor': [entrega.valor_total for entrega in entregas]
    }
    df = pd.DataFrame(data)

    # Agrupando por 'Funcionario' e somando os valores
    df_grouped = df.groupby('Funcionario').sum().reset_index()

    # Convertendo os dados para JSON
    chart_data = {
        'labels': df_grouped['Funcionario'].tolist(),
        'values': df_grouped['Valor'].tolist()
    }

    return jsonify(chart_data)