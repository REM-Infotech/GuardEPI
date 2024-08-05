from flask import render_template, request
from flask_login import login_required
from app import app
from app.models.EPI import GradeEPI, ProdutoEPI
from app.Forms.globals import IMPORTEPIForm
from app.Forms.create import InsertEstoqueForm

from app.misc import format_currency_brl

def set_choices() -> list[tuple[str, str]]:

    dbase = ProdutoEPI.query.all()

    return [(epi.nome_epi, epi.nome_epi) for epi in dbase]

@app.route("/Estoque")
@login_required
def Estoque():

    database = GradeEPI.query.all()
    title = request.endpoint.capitalize()
    DataTables = 'js/EstoqueTable.js'
    page = "pages/Estoque.html"
    form = InsertEstoqueForm()

    form.nome_epi.choices.extend(set_choices())

    importForm = IMPORTEPIForm()
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, form=form, importForm=importForm,
                           format_currency_brl=format_currency_brl)
    
@app.route("/Grade")
@login_required
def Grade():
    
    return render_template("index.html")
    
@app.route("/Entradas")
@login_required
def Entradas():

    return render_template("index.html")
