from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from app.forms import CadastroCategorias

template_folder = Path(__file__).parent.resolve().joinpath("templates")
categoria = Blueprint("categoria", __name__, template_folder=template_folder)


@categoria.route("/categorias", methods=["GET"])
@login_required
def categorias():
    form = CadastroCategorias()

    page = "categorias.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
