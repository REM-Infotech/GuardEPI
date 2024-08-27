from flask import render_template, request, url_for
from flask_login import login_required

from typing import Type
from datetime import datetime
from wtforms import DateField, SelectField
from sqlalchemy import LargeBinary
from sqlalchemy import Float

from app import app
from app import db

from app.models import Fornecedores as fornecedores
from app.models import Marcas as marcas
from app.models import ClassesEPI
from app.models import ModelosEPI


from app.Forms import (CadastroEPIForm, CadastroClasses, CadastroFonecedores, 
                       CadastroMarcas, CadastroModelos)

from app.Forms import IMPORTEPIForm, EditItemProdutoForm

from app.models import ProdutoEPI
from app.misc import format_currency_brl
from app.decorators import read_perm, set_endpoint

tipo = db.Model

def get_models(tipo) -> Type[tipo]:

    models = {"equipamentos": ProdutoEPI,
              'fornecedores': fornecedores,
              'marcas': marcas,
              'modelos': ModelosEPI,
              'classes': ClassesEPI}

    return models[tipo]

@app.route("/Equipamentos")
@login_required
@set_endpoint
#@read_perm
def Equipamentos():

    importForm = IMPORTEPIForm()
    form = CadastroEPIForm()
    page = f"pages/epi/{request.endpoint.lower()}.html"
    title = request.endpoint.capitalize()
    database = get_models(request.endpoint.lower()).query.all()
    DataTables = 'js/DataTables/epi/EquipamentosTable.js'
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return render_template("index.html", page=page, title=title, form=form,
                           importForm=importForm, database=database,
                           format_currency_brl=format_currency_brl,
                           DataTables=DataTables, url_image=url)

@app.route("/SetEditarEPI/<item>", methods=["GET"])
@login_required
def SetEditarEPI(item: int):
    
    form = EditItemProdutoForm
    model = ProdutoEPI
    database = model.query.filter(model.id == item).first()
    route = request.referrer.replace("https://", "").replace("http://", "")
    route = route.split("/")[1].lower()
    
    if "?" in route:
        route = route.split("?")[0]

    form = form(**{
        'nome_epi': database.nome_epi,
        'ca': database.ca,
        'cod_ca': database.cod_ca,
        'valor_unitario': format_currency_brl(database.valor_unitario),
        'periodicidade_item': database.periodicidade_item,
        'qtd_entregar': database.qtd_entregar,
        'fornecedor': database.fornecedor,
        'marca': database.marca,
        'modelo': database.modelo,
        'tipo_epi': database.tipo_epi,
        'vencimento': database.vencimento
    })
        
    url = ""
    if any(route == tipos for tipos in ["empresas", "equipamentos"]):

        image_name = form.filename.data
        if image_name is None:

            url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
            form.filename.data = url

        else:
            url = url_for('serve_img', index = item,
                          md=route, _external=True, _scheme='https')

    grade_results = f"pages/forms/{route}/edit.html"
    return render_template(grade_results, form=form,  url=url, tipo=route, id=item)

@app.route("/Fornecedores", methods = ["GET"])
@login_required
@set_endpoint
#@read_perm
def Fornecedores():

    form = CadastroFonecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database)

@app.route("/Marcas", methods = ["GET"])
@login_required
@set_endpoint
#@read_perm
def Marcas():
    
    form = CadastroMarcas()    
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database)
    
@app.route("/Modelos", methods = ["GET"])
@login_required
@set_endpoint
#@read_perm
def Modelos():
    
    form = CadastroModelos()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database)
    
@app.route("/Classes", methods = ["GET"])
@login_required
@set_endpoint
#@read_perm
def Classes():

    form = CadastroClasses()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database)
