from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import CadastroMarcas
from app.models import Marcas

from . import epi


@epi.route("/marcas", methods=["GET"])
@login_required
def marcas():

    page = "marcas.html"
    database = Marcas.query.all()
    return render_template("index.html", page=page, database=database)


@epi.route("/marca/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_marca():

    endpoint = "marca"
    act = "Cadastro"
    form = CadastroMarcas()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit":
                to_add.update({key: value})

        classe = Marcas(**to_add)
        db.session.add(classe)
        db.session.commit()
        flash("Marca cadastrada com sucesso!", "success")
        return redirect(url_for("epi.marcas"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/marca/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_marca(id):

    endpoint = "marca"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroMarcas()

    classe = db.session.query(Marcas).filter(Marcas.id == id).first()

    if request.method == "GET":
        form = CadastroMarcas(**classe.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(classe, key, value)

        db.session.commit()

        flash("Marca editada com sucesso!", "success")
        return redirect(url_for("epi.marcas"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/marcas/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_marca(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    classe = db.session.query(Marcas).filter(Marcas.id == id).first()

    db.session.delete(classe)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
