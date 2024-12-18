
from flask import render_template
from flask_login import login_required

from app.forms import CadastroMarcas

from . import epi


@epi.route("/marcas", methods=["GET"])
@login_required
def marcas():
    form = CadastroMarcas()

    page = "marcas.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)
