from flask import render_template, request, make_response, jsonify
from flask_login import login_required
from app import app
from app.models.EPI import RegistrosEPI
from app.decorators import set_endpoint

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
    
    database = RegistrosEPI.query.all()
    title = request.endpoint.capitalize()
    page = "pages/dashboard.html"
    DataTables = 'js/DashboardTable.js'
    
    resp = make_response(render_template("index.html", page = page, title = title, 
                           database = database, DataTables = DataTables))
    

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
