from flask import render_template, request
from flask_login import login_required
from app import app
from app.Forms import (CadastroEPIForm, CadastroClasses, CadastroFonecedores, 
                       CadastroMarcas, CadastroModelos)
from app.Forms import IMPORTEPIForm

from app.models import ProdutoEPI
from app.misc import format_currency_brl

from app.decorators import read_perm, set_endpoint

@app.route("/Equipamentos")
@login_required
@set_endpoint
@read_perm
def Equipamentos():

    importForm = IMPORTEPIForm()
    form = CadastroEPIForm()
    page = f"pages/epi/{request.endpoint.lower()}.html"
    title = request.endpoint.capitalize()
    database = ProdutoEPI.query.all()
    DataTables = 'js/DataTables/epi/EquipamentosTable.js'
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return render_template("index.html", page=page, title=title, form=form,
                           importForm=importForm, database=database,
                           format_currency_brl=format_currency_brl,
                           DataTables=DataTables, url_image=url)
    
@app.route("/Fornecedores", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Fornecedores():

    form = CadastroFonecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables)

@app.route("/Marcas", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Marcas():
    
    form = CadastroMarcas()    
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables)
    
@app.route("/Modelos", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Modelos():
    
    form = CadastroModelos()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables)
    
@app.route("/Classes", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Classes():

    form = CadastroClasses()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables)
