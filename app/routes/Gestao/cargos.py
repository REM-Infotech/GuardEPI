from flask import render_template, request
from flask_login import login_required
from app import app

from app.Forms.globals import IMPORTEPIForm
from app.Forms.create import CadastroCargo

from app.models.Funcionários import Cargos
from app.decorators import read_perm, set_endpoint



@app.route("/cargos")
@login_required
@set_endpoint
@read_perm
def cargos():

    importForm = IMPORTEPIForm()
    page = f"pages/Gestao/{request.endpoint.lower()}.html"
    database = Cargos.query.all()
    DataTables = f'js/DataTables/gestao/{request.endpoint.capitalize()}Table.js'
    form = CadastroCargo()
    return render_template("index.html", page=page, form=form, database=database,
                           DataTables=DataTables, importForm=importForm)
