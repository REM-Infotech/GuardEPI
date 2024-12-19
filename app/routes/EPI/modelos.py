from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import CadastroModelos
from app.models import ModelosEPI

from . import epi


@epi.route("/modelos", methods=["GET"])
@login_required
def modelos():

    page = "modelos.html"
    database = ModelosEPI.query.all()
    return render_template("index.html", page=page, database=database)


@epi.route("/modelos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_modelos():

    endpoint = "modelos"
    act = "Cadastro"
    form = CadastroModelos()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        classe = ModelosEPI(**to_add)
        db.session.add(classe)
        db.session.commit()
        flash("modelos cadastrada com sucesso!", "success")
        return redirect(url_for("epi.modeloss"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/modelos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_modelos(id):

    endpoint = "modelos"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroModelos()

    classe = db.session.query(ModelosEPI).filter(ModelosEPI.id == id).first()

    if request.method == "GET":
        form = CadastroModelos(**classe.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(classe, key, value)

        db.session.commit()

        flash("modelos editada com sucesso!", "success")
        return redirect(url_for("epi.modeloss"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/modeloss/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_modelos(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    classe = db.session.query(ModelosEPI).filter(ModelosEPI.id == id).first()

    db.session.delete(classe)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
