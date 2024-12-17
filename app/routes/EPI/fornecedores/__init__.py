from pathlib import Path

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroFornecedores
from app.models import get_models

template_folder = Path(__file__).joinpath("templates")
fornece = Blueprint("fornece", __name__, template_folder=template_folder)


@fornece.route("/fornecedores", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def fornecedores():
    form = CadastroFornecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
