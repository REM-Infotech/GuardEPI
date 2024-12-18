from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from app.forms import CadastroModelos

template_folder = Path(__file__).parent.resolve().joinpath("templates")
modelo = Blueprint("modelo", __name__, template_folder=template_folder)


@modelo.route("/modelos", methods=["GET"])
@login_required
def modelos():

    form = CadastroModelos()

    page = "modelos.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
