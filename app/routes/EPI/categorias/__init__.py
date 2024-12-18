from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroCategorias

template_folder = Path(__file__).parent.resolve().joinpath("templates")
categoria = Blueprint("categoria", __name__, template_folder=template_folder)


@categoria.route("/categorias", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def categorias():
    form = CadastroCategorias()
    DataTables = "js/DataTables/DataTables.js"
    page = "categorias.html"
    database = []
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
