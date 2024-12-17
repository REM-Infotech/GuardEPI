from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroCategorias
from app.models import get_models

categoria = Blueprint("categoria", __name__)


@categoria.route("/categorias", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def categorias():
    form = CadastroCategorias()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
