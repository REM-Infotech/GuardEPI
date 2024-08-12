from flask import render_template, request
from flask_login import login_required

from app.Forms.globals import IMPORTEPIForm
from app.Forms.create import CadastroEmpresa

from app.models.Funcionários import Empresa

from app import app
from app.decorators import read_perm, set_endpoint


@app.route("/Empresas", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Empresas():

    importForm = IMPORTEPIForm()
    form = CadastroEmpresa()
    database = Empresa.query.all()
    DataTables = f'js/DataTables/gestao/{request.endpoint.capitalize()}Table.js'
    page = f"pages/Gestao/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database, 
                           importForm=importForm)

