from flask import *
from flask_login import *
from app import app
from app import db
from app.Forms import *
from app.models import *
from app.misc import *
from app.routes.CRUD.create import *
from app.routes.CRUD.update import *
from app.routes.CRUD.delete import *
from app.routes.EPI.emitir_cautela import *
from app.routes.Gestao.set import config_form
from app.decorators import read_perm

def set_choices() -> list[tuple[str, str]]:

    dbase = ProdutoEPI.query.all()

    return [(epi.nome_epi, epi.nome_epi) for epi in dbase]


@app.route("/funcionarios")
@login_required
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
