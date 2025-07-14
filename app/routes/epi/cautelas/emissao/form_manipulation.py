import json
import os
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from quart import Response, abort, make_response, render_template, request, session
from quart import current_app as app
from quart_auth import login_required

from app.decorators import create_perm
from app.forms.epi import Cautela
from app.models.EPI.estoque import EstoqueEPI, EstoqueGrade
from app.routes.epi import estoque_bp


@estoque_bp.before_request
async def setgroups() -> None:
    if request.endpoint == "estoque.emitir_cautela" and request.method == "GET":
        session["uuid_Cautelas"] = str(uuid4())
        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json"
        )

        if os.path.exists(pathj):
            os.remove(pathj)

        json_obj = json.dumps([])

        with open(pathj, "w") as f:
            f.write(json_obj)


@estoque_bp.route("/add_itens", methods=["GET", "POST"])
@login_required
@create_perm
async def add_itens() -> Response:
    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        form = Cautela()

        nome_epi = form.nome_epi.data
        grade_epi = form.tipo_grade.data

        item_cautela = {
            "NOME_EPI": nome_epi,
            "GRADE": form.tipo_grade.data,
            "QTD": form.qtd_entregar.data,
        }

        data_estoque = (
            db.session.query(EstoqueEPI).filter(EstoqueEPI.nome_epi == nome_epi).first()
        )
        estoque_grade = (
            db.session.query(EstoqueGrade)
            .filter(
                EstoqueGrade.nome_epi == nome_epi,
                EstoqueGrade.grade == grade_epi,
            )
            .first()
        )

        if estoque_grade is not None:
            if all([estoque_grade.qtd_estoque == 0, data_estoque.qtd_estoque == 0]):
                return await make_response(
                    await render_template(
                        "forms/cautela/not_estoque.html", epi_name=nome_epi
                    )
                )

        elif estoque_grade is None:
            return await make_response(
                await render_template(
                    "forms/cautela/not_estoque.html",
                    message="EPI não registrada no estoque!",
                )
            )

        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json"
        )

        with open(pathj, "rb") as f:
            list_epis: list[dict[str, str | int]] = json.load(f)

        item_cautela.update({"ID": len(list_epis)})

        list_epis.append(item_cautela)
        json_obj = json.dumps(list_epis)

        with open(pathj, "w") as f:
            f.write(json_obj)

        item_html = await render_template(
            "forms/cautela/add_items.html", item=list_epis
        )

        # Retorna o HTML do item
        return await make_response(item_html)
    except Exception as e:
        abort(500, description=str(e))


@estoque_bp.route("/remove-itens", methods=["GET", "POST"])
@login_required
@create_perm
async def remove_itens() -> Response:
    pathj = os.path.join(app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json")
    json_obj = json.dumps([])

    with open(pathj, "w") as f:
        f.write(json_obj)

    item_html = await render_template("forms/cautela/add_items.html")
    return await make_response(item_html)


@estoque_bp.post("/get_grade")
@login_required
@create_perm
async def get_grade() -> Response:
    try:
        form = Cautela()
        lista = []
        dbase = EstoqueGrade.query.filter_by(nome_epi=form.nome_epi.data).all()
        for query in dbase:
            lista.append((query.grade, query.grade))
        form.tipo_grade.choices.extend(lista)

        page = "forms/cautela/get_grade.html"
        return await make_response(await render_template(page, form=form))
    except Exception as e:
        abort(500, description=str(e))
