from flask import Flask
from deep_translator import GoogleTranslator
from flask import redirect, render_template, url_for
from werkzeug.exceptions import HTTPException

from app.routes.dashboard import dash
from app.routes.cargos import cargo_bp
from app.routes.EPI import (
    categoria,
    cautelas,
    equip,
    estoque,
    fornecedor,
    marca,
    modelo,
)


def register_routes(app: Flask):

    with app.app_context():

        blueprints = [
            dash,
            cargo_bp,
            categoria,
            cautelas,
            equip,
            estoque,
            fornecedor,
            marca,
            modelo,
        ]

        for blueprint in blueprints:
            app.register_routes(blueprint)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        tradutor = GoogleTranslator(source="en", target="pt")
        name = tradutor.translate(error.name)
        desc = tradutor.translate(error.description)

        if error.code == 405:
            return redirect(url_for("dash.dashboard"))

        return (
            render_template(
                "handler/index.html", name=name, desc=desc, code=error.code
            ),
            error.code,
        )


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
