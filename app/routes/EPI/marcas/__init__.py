from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from app.forms import CadastroMarcas

template_folder = Path(__file__).parent.resolve().joinpath("templates")
marca = Blueprint("marca", __name__, template_folder=template_folder)


@marca.route("/marcas", methods=["GET"])
@login_required
def marcas():
    form = CadastroMarcas()

    page = "marcas.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
