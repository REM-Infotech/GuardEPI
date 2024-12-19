from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import CadastroCargo
from app.models import Cargos

from . import corp


@corp.route("/cargos")
@login_required
def cargos():

    try:
        page = "cargos.html"
        database = Cargos.query.all()

        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/cargos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_cargos():

    endpoint = "Cargos"
    act = "Cadastro"
    form = CadastroCargo()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key.lower() == "csrf_token" or key.lower() == "submit":
                continue

            to_add.update({key: value})

        cargos = Cargos(**to_add)
        db.session.add(cargos)
        db.session.commit()
        flash("Cargo cadastrado com sucesso!", "success")
        return redirect(url_for("corp.cargos"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@corp.route("/cargos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cargos(id):

    endpoint = "cargos"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroCargo()

    cargos = db.session.query(Cargos).filter(Cargos.id == id).first()

    if request.method == "GET":
        form = CadastroCargo(**cargos.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(cargos, key, value)

        db.session.commit()

        flash("Cargo editado com sucesso!", "success")
        return redirect(url_for("corp.cargos"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@corp.route("/cargoss/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_cargos(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    cargos = db.session.query(Cargos).filter(Cargos.id == id).first()

    db.session.delete(cargos)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
