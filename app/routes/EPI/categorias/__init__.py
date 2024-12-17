import os
from pathlib import Path

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroCategorias

template_folder = os.path.join(Path(__file__).parent.resolve(), "templates")
categoria = Blueprint("categoria", __name__, template_folder=template_folder)


@categoria.route("/categorias", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def categorias():
    form = CadastroCategorias()
    DataTables = "js/DataTables/DataTables.js"
    page = f"{request.endpoint.lower()}.html"
    database = []
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
