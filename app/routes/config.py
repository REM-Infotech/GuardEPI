from flask import *
from flask_login import *
from app import app
from app.models import *

@app.route("/config", methods = ["GET"])
@login_required
def config():
    
    """
    ## Rota config

    ### Returns:
        title: titulo da página
        page: página a ser renderizada
        DataTables: JS Datatables para a página
        
    """
    
    database = Users.query.all()
    title = request.endpoint.capitalize()
    # page = "pages/config.html"
    # DataTables = 'js/configTable.js'
    
    return render_template("index.html", title = title, database = database)