from flask import render_template
from flask_login import login_required

from app.forms import CadastroModelos

from . import epi


@epi.route("/modelos", methods=["GET"])
@login_required
def modelos():

    form = CadastroModelos()

    page = "modelos.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
