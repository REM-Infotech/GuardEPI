from flask import abort, render_template
from flask_login import login_required

from app.forms.create import CadastroDepartamentos
from app.models.Funcionários import Departamento

from . import corp


@corp.route("/Departamentos")
@login_required
def Departamentos():
    try:

        form = CadastroDepartamentos()
        page = "departamentos.html"
        database = Departamento.query.all()

        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))
