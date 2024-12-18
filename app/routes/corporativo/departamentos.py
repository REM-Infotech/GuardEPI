from flask import abort, render_template
from flask_login import login_required

from . import corp
from app.forms.create import CadastroDepartamentos
from app.models.Funcionários import Departamento


@corp.route("/Departamentos")
@login_required
def Departamentos():
    try:

        form = CadastroDepartamentos()
        page = ""
        database = Departamento.query.all()
        DataTables = ""
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
            DataTables=DataTables,
        )
    except Exception as e:
        abort(500, description=str(e))
