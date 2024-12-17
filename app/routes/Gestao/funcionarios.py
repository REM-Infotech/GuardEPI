from flask import abort, render_template, request
from flask_login import login_required

from app import app
from app.decorators import read_perm, set_endpoint
from app.forms import CadastroFuncionario, IMPORTEPIForm
from app.models.Funcionários import Funcionarios


@app.route("/funcionarios")
@login_required
@set_endpoint
@read_perm
def funcionarios():
    try:
        form = CadastroFuncionario()
        importForm = IMPORTEPIForm()
        DataTables = f"js/DataTables/gestao/{request.endpoint.capitalize()}Table.js"
        page = f"pages/Gestao/{request.endpoint.lower()}.html"
        database = Funcionarios.query.all()
        return render_template(
            "index.html",
            page=page,
            DataTables=DataTables,
            importForm=importForm,
            database=database,
            form=form,
        )
    except Exception as e:
        abort(500, description=str(e))
