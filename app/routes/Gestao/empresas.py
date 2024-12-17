from flask import abort, render_template, request
from flask_login import login_required

from app import app
from app.decorators import read_perm, set_endpoint
from app.forms.create import CadastroEmpresa
from app.forms.globals import IMPORTEPIForm
from app.models.Funcionários import Empresa


@app.route("/Empresas", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Empresas():
    try:
        importForm = IMPORTEPIForm()
        form = CadastroEmpresa()
        database = Empresa.query.all()
        DataTables = f"js/DataTables/gestao/{request.endpoint.capitalize()}Table.js"
        page = f"pages/Gestao/{request.endpoint.lower()}.html"
        return render_template(
            "index.html",
            page=page,
            form=form,
            DataTables=DataTables,
            database=database,
            importForm=importForm,
        )

    except Exception as e:
        abort(500, description=str(e))
