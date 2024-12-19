from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import CadastroFornecedores
from app.models import Fornecedores

from . import epi


@epi.route("/fornecedores", methods=["GET"])
@login_required
def fornecedores():
    form = CadastroFornecedores()

    page = "fornecedores.html"
    database = []
    return render_template("index.html", page=page, form=form, database=database)


@epi.route("/fornecedores/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_fornecedores():

    endpoint = "fornecedores"
    act = "Cadastro"
    form = CadastroFornecedores()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        fornecedor = Fornecedores(**to_add)
        db.session.add(fornecedor)
        db.session.commit()
        flash("Fornecedor cadastrado com sucesso!", "success")
        return redirect(url_for("epi.fornecedores"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/fornecedores/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_fornecedores(id):

    endpoint = "fornecedores"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroFornecedores()

    fornecedor = db.session.query(Fornecedores).filter(Fornecedores.id == id).first()

    if request.method == "GET":
        form = CadastroFornecedores(**fornecedor.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(fornecedor, key, value)

        db.session.commit()

        flash("Fornecedor editado com sucesso!", "success")
        return redirect(url_for("epi.fornecedores"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/fornecedores/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_fornecedores(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    fornecedor = db.session.query(Fornecedores).filter(Fornecedores.id == id).first()

    db.session.delete(fornecedor)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
