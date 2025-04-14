from pathlib import Path
from typing import Type, TypeVar
from flask import (
    Flask,
    Response,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
import pandas
from tqdm import tqdm
from werkzeug.exceptions import HTTPException

from app.models.EPI.equipamento import ProdutoEPI
from app.models.EPI.estoque import EstoqueEPI, EstoqueGrade

from .auth import auth
from .config import config
from .corporativo import corp
from .dashboard import dash
from .epi import epi, estoque_bp
from .index import index as ind
from .serving import serve

type_db = TypeVar("model_db", bound=EstoqueEPI | EstoqueGrade)


def register_routes(app: Flask) -> None:
    """
    Register routes and error handlers for the Flask application.
    This function registers blueprints and error handlers, and defines routes for terms of use and privacy policy PDFs.

    Args:
        app (Flask): The Flask application instance.

    Blueprints:

        - auth: Authentication blueprint.
        - dash: Dashboard blueprint.
        - corp: Corporate blueprint.
        - epi: EPI blueprint.
        - serve: Serve blueprint.

    Error Handlers:
        - HTTPException: Handles HTTP exceptions, translates error names to Portuguese, and redirects 405 errors to the dashboard.
    Routes:
        - /termos_uso (GET): Serves the "Termos de Uso.pdf" file from the configured PDF path.
        - /politica_privacidade (GET): Serves the "Política de Privacidade.pdf" file from the configured PDF path.
    """

    blueprints = [auth, dash, corp, epi, serve, ind, estoque_bp, config]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error) -> Response:
        """
        Handles HTTP exceptions by translating the error name to Portuguese and rendering an error template.
        Args:
            error (HTTPException): The HTTP exception that was raised.
        Returns:
            Response: A Flask response object with the rendered error template and the appropriate HTTP status code.
        """
        # tradutor = GoogleTranslator(source="en", target="pt")
        # name = tradutor.translate(error.name)
        # desc = tradutor.translate(error.description)

        name: str = "Erro interno"
        desc: str = "Erro do sistema"

        if error.code == 500 and "já cadastrado" not in getattr(
            error, "desc", "Erro do sistema"
        ):
            desc: str = "Erro do sistema"

        if error.code == 405:
            return make_response(redirect(url_for("dash.dashboard")))

        return make_response(
            render_template(
                "handler/index.html", name=name, desc=desc, code=error.code
            ),
            error.code,
        )

    @app.route("/importar_planilha_route", methods=["POST"])
    def importar_planilha_route() -> None:
        request_json = request.json
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        path_xlsx = Path(request_json.get("file")).resolve()

        dataframe = pandas.read_excel(path_xlsx).fillna("")

        novo_dicionario: dict[str, dict[str, int]] = {}

        data_ = dataframe.to_dict(orient="records")

        for item in dataframe.to_dict(orient="records"):
            if item["EPI"] not in novo_dicionario:
                grades_ = {}
                grades = list(
                    filter(lambda x: str(x.get("EPI", "")) == str(item["EPI"]), data_)
                )

                total = 0

                for i in grades:
                    grades_.update({str(i.get("GRADE")): int(i.get("FISICO"))})
                    total += int(i.get("FISICO"))

                grades_.update({"TOTAL": total})

                novo_dicionario.update({item["EPI"]: grades_})

        all_estoque = db.session.query(EstoqueEPI).all()
        all_estoque_grade = db.session.query(EstoqueGrade).all()
        all_produtos = db.session.query(ProdutoEPI).all()

        def func_filt_it(x: Type[type_db]) -> bool:
            in_db = x.nome_epi.lower().strip().replace(" ", "")
            return in_db == stripe_k

        def func_filt_grd(x: Type[type_db]) -> bool:
            in_db = str(x.grade.lower().strip().replace(" ", ""))
            return in_db == stripe_grd

        for key, value in tqdm(novo_dicionario.items()):
            stripe_k = key.strip().lower().replace(" ", "")

            produto_check = list(filter(lambda x: func_filt_it(x), all_produtos))
            grades_filtered = list(
                filter(
                    lambda x: func_filt_it(x),
                    all_estoque_grade,
                )
            )
            id_item_estoque = list(
                filter(
                    lambda x: func_filt_it(x),
                    all_estoque,
                )
            )

            if len(produto_check) == 0:
                continue

            for k, v in value.items():
                if k == "TOTAL":
                    continue

                stripe_grd = k.strip().lower().replace(" ", "")

                id_item_estoque_grade = []
                if len(grades_filtered) > 0:
                    id_item_estoque_grade = list(
                        filter(
                            lambda x: func_filt_grd(x),
                            grades_filtered,
                        )
                    )

                if len(id_item_estoque_grade) > 0:
                    item_grade = (
                        db.session.query(EstoqueGrade)
                        .filter(EstoqueGrade.id == id_item_estoque_grade[-1].id)
                        .first()
                    )
                    item_grade.qtd_estoque = v
                    db.session.commit()
                    continue

                novo_item = EstoqueGrade(
                    nome_epi=key,
                    tipo_qtd=item["TIPO_QTD"],
                    qtd_estoque=v,
                    grade=k.upper(),
                )
                db.session.add(novo_item)
                db.session.commit()

            if len(id_item_estoque) > 0:
                item_estoque = (
                    db.session.query(EstoqueEPI)
                    .filter(EstoqueEPI.id == id_item_estoque[-1].id)
                    .first()
                )
                item_estoque.qtd_estoque = value.get("TOTAL")
                db.session.commit()
                continue

            novo_item_estoque = EstoqueEPI(
                nome_epi=key,
                tipo_qtd="Unidade",
                qtd_estoque=value.get("TOTAL"),
            )
            db.session.add(novo_item_estoque)
            db.session.commit()

        return make_response(jsonify({"status": "ok"}), 200)


# from app import app
# import json
# import os
# from flask import request

# @app.before_request
# def save_endpoints():

#     rar = request.url_rule.map._rules

#     endpoints = {}
#     for item in rar:

#         endpoints.update({item.endpoint: item.endpoint})

#     json_object = json.dumps(endpoints, indent=4)
#     with open("myJsn.json", "w") as outfile:
#         outfile.write(json_object)
