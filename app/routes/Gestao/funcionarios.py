from flask import render_template, request
from flask_login import login_required
from app import app


from app.models.Funcionários import Funcionarios
from app.Forms.globals import IMPORTEPIForm

from app.routes.CRUD.create import CadastroFuncionario
from app.routes.Gestao.set import config_form

from app.decorators import read_perm, set_endpoint


@app.route("/funcionarios")
@login_required
@set_endpoint
@read_perm
def funcionarios():

    form = config_form(CadastroFuncionario())
    importForm = IMPORTEPIForm()
    import_endpoint = 'importacao_corporativo'
    DataTables = f'js/{request.endpoint.capitalize()}Table.js'
    page = f"pages/{request.endpoint.lower()}.html"
    database = Funcionarios.query.all()
    return render_template("index.html", page=page, DataTables=DataTables, import_endpoint=import_endpoint,
                           importForm=importForm, database=database, form=form)
