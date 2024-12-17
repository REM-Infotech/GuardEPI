import os
from pathlib import Path

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroFornecedores

template_folder = os.path.join(Path(__file__).parent.resolve(), "templates")
fornecedor = Blueprint("fornecedor", __name__, template_folder=template_folder)


@fornecedor.route("/fornecedores", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def fornecedores():
    form = CadastroFornecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"{request.endpoint.lower()}.html"
    database = []
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
