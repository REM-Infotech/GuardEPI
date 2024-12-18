
from flask import render_template
from flask_login import login_required

from app.forms import CadastroFornecedores

from . import epi


@epi.route("/fornecedores", methods=["GET"])
@login_required
def fornecedores():
    form = CadastroFornecedores()

    page = "fornecedores.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
