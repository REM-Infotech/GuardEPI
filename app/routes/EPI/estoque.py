from flask import render_template, request
from flask_login import login_required
from app import app
from app.models.EPI import GradeEPI, ProdutoEPI, RegistroEntradas, EstoqueEPI
from app.Forms.globals import IMPORTEPIForm
from app.Forms.create import InsertEstoqueForm, CadastroGrade

from app.misc import format_currency_brl
from app.decorators import read_perm, set_endpoint

def set_choices() -> list[tuple[str, str]]:

    dbase = ProdutoEPI.query.all()

    return [(epi.nome_epi, epi.nome_epi) for epi in dbase]

@app.route("/Estoque")
@login_required
@set_endpoint
@read_perm
def Estoque():

    database = GradeEPI.query.all()
    title = request.endpoint.capitalize()
    DataTables = 'js/DataTables/epi/EstoqueTable.js'
    page = f"pages/epi/{request.endpoint.lower()}.html"
    form = InsertEstoqueForm()

    form.nome_epi.choices.extend(set_choices())

    importForm = IMPORTEPIForm()
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, form=form, importForm=importForm,
                           format_currency_brl=format_currency_brl)
    
@app.route("/Grade")
@login_required
def Grade():
    
    title = "Grades"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    DataTables = 'js/DataTables/epi/grade.js'
    form = CadastroGrade()
    importForm = IMPORTEPIForm()
    database = EstoqueEPI.query.all()
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, form=form, importForm=importForm,
                           format_currency_brl=format_currency_brl)
    
@app.route("/Entradas")
@login_required
def Entradas():

    title = "Relação de Entradas EPI"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    importForm = IMPORTEPIForm()
    database = RegistroEntradas.query.all()
    DataTables = 'js/DataTables/epi/entradas.js'
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, importForm=importForm)
