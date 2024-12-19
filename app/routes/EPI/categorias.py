from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

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
def cadastrar_categoria():

    endpoint = "Categoria"
    act = "Cadastro"
    form = CadastroCategorias()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit":
                to_add.update({key: value})

        classe = ClassesEPI(**to_add)
        db.session.add(classe)
        db.session.commit()
        flash("Categoria cadastrada com sucesso!", "success")
        return redirect(url_for("epi.categorias"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):

    endpoint = "Categoria"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroCategorias()

    classe = db.session.query(ClassesEPI).filter(ClassesEPI.id == id).first()

    if request.method == "GET":
        form = CadastroCategorias(**classe.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(classe, key, value)

        db.session.commit()

        flash("Categoria editada com sucesso!", "success")
        return redirect(url_for("epi.categorias"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/categorias/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_categoria(id: int):
    # Logic to delete category from the database
    pass
    return redirect(url_for("categoria.categorias"))
