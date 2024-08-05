from flask import render_template, request
from flask_login import login_required
from app import app

from app.Forms.globals import IMPORTEPIForm
from app.Forms.create import CadastroDepartamentos

from app.models.Funcionários import Departamento
from app.decorators import read_perm, set_endpoint


@app.route("/Departamentos")
@login_required
@set_endpoint
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
