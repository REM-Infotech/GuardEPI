from flask import abort, render_template, request
from flask_login import login_required

from app import app
from app.decorators import read_perm, set_endpoint
from app.Forms.create import CadastroDepartamentos
from app.Forms.globals import IMPORTEPIForm
from app.models.Funcionários import Departamento


@app.route("/Departamentos")
@login_required
@set_endpoint
@read_perm
def Departamentos():
    try:
        importForm = IMPORTEPIForm()
        form = CadastroDepartamentos()
        page = f"pages/Gestao/{request.endpoint.lower()}.html"
        database = Departamento.query.all()
        DataTables = f"js/DataTables/gestao/{request.endpoint.capitalize()}Table.js"
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
            DataTables=DataTables,
            importForm=importForm,
        )
    except Exception as e:
        abort(500, description=str(e))
