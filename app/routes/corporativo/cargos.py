from . import corp

from flask import abort, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms.create import CadastroCargo

from app.models.Funcionários import Cargos


@corp.route("/cargos")
@login_required
def cargos():

    try:
        page = ".html"
        database = Cargos.query.all()
        DataTables = ""
        form = CadastroCargo()
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
            DataTables=DataTables,
        )
    except Exception as e:
        abort(500, description=str(e))
