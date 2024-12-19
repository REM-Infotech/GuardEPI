from flask import abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.forms import CadastroDepartamentos
from app.models import Departamento

from . import corp


@corp.route("/Departamentos")
@login_required
def Departamentos():
    try:

        page = "departamentos.html"
        database = Departamento.query.all()

        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/Departamentos/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_departamentos():

    endpoint = "Departamentos"
    act = "Cadastro"
    form = CadastroDepartamentos()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit":
                to_add.update({key: value})

        Departamentos = Departamento(**to_add)
        db.session.add(Departamentos)
        db.session.commit()
        flash("Departamentos cadastrada com sucesso!", "success")
        return redirect(url_for("epi.Departamentoss"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@corp.route("/Departamentos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_departamentos(id):

    endpoint = "Departamentos"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroDepartamentos()

    Departamentos = db.session.query(Departamento).filter(Departamento.id == id).first()

    if request.method == "GET":
        form = CadastroDepartamentos(**Departamentos.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(Departamentos, key, value)

        db.session.commit()

        flash("Departamentos editada com sucesso!", "success")
        return redirect(url_for("epi.Departamentoss"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@corp.route("/Departamentoss/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_departamentos(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    Departamentos = db.session.query(Departamento).filter(Departamento.id == id).first()

    db.session.delete(Departamentos)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
