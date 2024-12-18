from flask import redirect, render_template, url_for
from flask_login import login_required

from app.forms import CadastroCategorias
from app.models import ClassesEPI

from . import epi


@epi.route("/categorias", methods=["GET"])
@login_required
def categorias():
    form = CadastroCategorias()

    page = "categorias.html"
    database = ClassesEPI.query.all()

    return render_template("index.html", page=page, form=form, database=database)


@epi.route("/categorias/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar():
    form = CadastroCategorias()
    if form.validate_on_submit():
        # Logic to add category to the database
        pass
    return render_template("index.html", page="form_base.html", form=form)


@epi.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    form = CadastroCategorias()
    if form.validate_on_submit():
        # Logic to update category in the database
        pass
    # Logic to load category data into form
    return render_template("index.html", page="form_base.html", form=form)


@epi.route("/categorias/deletar/<int:id>", methods=["POST"])
@login_required
def deletar(id: int):
    # Logic to delete category from the database
    pass
    return redirect(url_for("categoria.categorias"))
