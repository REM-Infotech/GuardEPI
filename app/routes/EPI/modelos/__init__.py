from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroModelos
from app.models import get_models

modelo = Blueprint("modelo", __name__)


@modelo.route("/modelos", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def modelos():
    form = CadastroModelos()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
