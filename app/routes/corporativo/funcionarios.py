from flask import abort, render_template
from flask_login import login_required

from app.forms import CadastroFuncionario
from app.models.Funcionários import Funcionarios

from . import corp


@corp.get("/funcionarios")
@login_required
def funcionarios():
    try:

        page = "funcionarios.html"
        database = Funcionarios.query.all()
        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/funcionarios/cadastro")
@login_required
def cadastro():

    form = CadastroFuncionario()

    if form.validate_on_submit():
        pass

    return render_template("index.html", form=form)
