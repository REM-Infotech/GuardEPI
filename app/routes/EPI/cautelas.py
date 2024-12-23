import json
import os
import uuid

from flask import abort
from flask import current_app as app
from flask import redirect, render_template, request, session, url_for
from flask_login import login_required

from app.decorators import create_perm
from app.forms import Cautela
from app.misc import format_currency_brl
from app.models import EstoqueGrade, RegistroSaidas, RegistrosEPI

from . import estoque_bp


@estoque_bp.before_request
def setgroups():

    if request.endpoint == "Cautelas":
        if not session.get("uuid_Cautelas", None):

            session["uuid_Cautelas"] = str(uuid.uuid4())
            pathj = os.path.join(
                app.config["TEMP_PATH"], f"{session["uuid_Cautelas"]}.json"
            )

            if os.path.exists(pathj):
                os.remove(pathj)

            json_obj = json.dumps([])

            with open(pathj, "w") as f:
                f.write(json_obj)


@estoque_bp.route("/add_itens", methods=["GET", "POST"])
@login_required
def add_itens():

    try:
        form = Cautela()
        list = [form.nome_epi.data, form.tipo_grade.data, form.qtd_entregar.data]

        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session["uuid_Cautelas"]}.json"
        )

        with open(pathj, "rb") as f:
            list_epis = json.load(f)

        list_epis.append(list)
        json_obj = json.dumps(list_epis)

        with open(pathj, "w") as f:
            f.write(json_obj)

        item_html = render_template("includes/add_items.html", item=list_epis)

        # Retorna o HTML do item
        return item_html
    except Exception as e:
        abort(500, description=str(e))


@estoque_bp.route("/remove-itens", methods=["GET", "POST"])
@login_required
def remove_itens():

    pathj = os.path.join(app.config["TEMP_PATH"], f"{session["uuid_Cautelas"]}.json")
    json_obj = json.dumps([])

    with open(pathj, "w") as f:
        f.write(json_obj)

    item_html = render_template("includes/add_items.html")
    return item_html


@estoque_bp.route("/registro_saidas", methods=["GET"])
@login_required
def registro_saidas():

    page = "registro_saidas.html"
    database = RegistroSaidas.query.all()
    title = request.endpoint.split(".")[1].capitalize().replace("_", " ")

    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        format_currency_brl=format_currency_brl,
    )


@estoque_bp.route("/cautelas", methods=["GET"])
@login_required
def cautelas():

    page = "cautelas.html"
    database = RegistrosEPI.query.all()
    title = request.endpoint.split(".")[1].capitalize()

    session["itens_lista_cautela"] = []
    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
    )


@estoque_bp.route("/get_grade", methods=["POST"])
@login_required
def get_grade():

    try:
        form = Cautela()
        lista = []
        dbase = EstoqueGrade.query.filter_by(nome_epi=form.nome_epi.data).all()
        for query in dbase:
            lista.append((query.grade, query.grade))
        form.tipo_grade.choices.extend(lista)

        page = "pages/forms/cautelas/get_grade.html"
        return render_template(page, form=form)
    except Exception as e:
        abort(500, description=str(e))


@estoque_bp.route("/emitir_cautela", methods=["GET", "POST"])
@login_required
@create_perm
def emitir_cautela():

    try:

        # db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = Cautela()
        if form.validate_on_submit():

            return redirect(url_for("estoque_bp.cautelas"))

        page = "forms/cautela/cautela_form.html"
        return render_template("index.html", page=page, form=form)

    except Exception as e:
        abort(500, description=str(e))
