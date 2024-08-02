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
from app.decorators import read_perm

def set_choices() -> list[tuple[str, str]]:

    dbase = ProdutoEPI.query.all()

    return [(epi.nome_epi, epi.nome_epi) for epi in dbase]


@app.route("/Departamentos")
@login_required
@read_perm
def Departamentos():

    importForm = IMPORTEPIForm()
    import_endpoint = 'importacao_corporativo'
    form = CadastroDepartamentos()
    page = f"pages/{request.endpoint.lower()}.html"
    database = Departamento.query.all()
    DataTables = f'js/{request.endpoint.capitalize()}Table.js'
    return render_template("index.html", page=page, form=form, database=database,
                           DataTables=DataTables, import_endpoint=import_endpoint,
                           importForm=importForm)
