from flask import render_template, request, make_response, jsonify
from flask_login import login_required
from app import app
from app.models.EPI import RegistrosEPI, RegistroEntradas
from app.decorators import set_endpoint
from app.misc import format_currency_brl

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
    
@app.route("/registros_saidas", methods = ["GET"])
def registros():
    
    """_summary_

    Returns:
        _type_: _description_
    """
    
    data = {"dias_semana": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
            "Saidas":  [5, 10 , 3, 25, 15],
            "media": 30}
    
    return jsonify(data)
