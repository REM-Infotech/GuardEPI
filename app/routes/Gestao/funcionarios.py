from flask import render_template, request
from flask_login import login_required
from app import app


from app.models.Funcionários import Funcionarios
from app.Forms.globals import IMPORTEPIForm

from app.routes.CRUD.create import CadastroFuncionario

from app.decorators import read_perm, set_endpoint


@app.route("/funcionarios")
@login_required
@set_endpoint
@read_perm
def funcionarios():

    form = CadastroFuncionario()
    importForm = IMPORTEPIForm()
    DataTables = f'js/DataTables/Gestao/{request.endpoint.capitalize()}Table.js'
    page = f"pages/Gestao/{request.endpoint.lower()}.html"
    database = Funcionarios.query.all()
    return render_template("index.html", page=page, DataTables=DataTables,
                           importForm=importForm, database=database, form=form)
