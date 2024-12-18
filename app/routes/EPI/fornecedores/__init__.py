from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from app.forms import CadastroFornecedores

template_folder = Path(__file__).parent.resolve().joinpath("templates")
fornecedor = Blueprint("fornecedor", __name__, template_folder=template_folder)


@fornecedor.route("/fornecedores", methods=["GET"])
@login_required
def fornecedores():
    form = CadastroFornecedores()

    page = "fornecedores.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
