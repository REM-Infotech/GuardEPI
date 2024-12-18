from flask import abort, render_template
from flask_login import login_required

from app.forms.create import CadastroEmpresa
from app.models.Funcionários import Empresa

from . import corp


@corp.route("/Empresas", methods=["GET"])
@login_required
def Empresas():
    try:

        form = CadastroEmpresa()
        database = Empresa.query.all()

        page = "empresas.html"
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
        )

    except Exception as e:
        abort(500, description=str(e))
