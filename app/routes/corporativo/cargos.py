from flask import abort, render_template
from flask_login import login_required

from app.forms.create import CadastroCargo
from app.models.Funcionários import Cargos

from . import corp


@corp.route("/cargos")
@login_required
def cargos():

    try:
        page = "cargos.html"
        database = Cargos.query.all()

        form = CadastroCargo()
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))
