from deep_translator import GoogleTranslator
from flask import (
    Flask,
    abort,
    make_response,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import HTTPException
from .auth import auth
from .corporativo import corp
from .dashboard import dash
from .serving import serve
from .epi import epi


def register_routes(app: Flask):

    with app.app_context():

        blueprints = [
            auth,
            dash,
            corp,
            epi,
            serve,
        ]

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        tradutor = GoogleTranslator(source="en", target="pt")
        name = tradutor.translate(error.name)
        # desc = tradutor.translate(error.description)

        if error.code == 405:
            return redirect(url_for("dash.dashboard"))

        return (
            render_template(
                "handler/index.html", name=name, desc="Erro Interno", code=error.code
            ),
            error.code,
        )

    @app.route("/termos_uso", methods=["GET"])
    def termos_uso():
        try:
            filename = "Termos de Uso.pdf"
            url = send_from_directory(app.config["PDF_PATH"], filename)
            # Crie a resposta usando make_response
            response = make_response(url)

            # Defina o tipo MIME como application/pdf
            response.headers["Content-Type"] = "application/pdf"
            return url

        except Exception as e:
            abort(500, description=str(e))

    @app.route("/politica_privacidade", methods=["GET"])
    def politica_privacidade():
        try:
            filename = "Política de Privacidade.pdf"
            url = send_from_directory(app.config["PDF_PATH"], filename)
            # Crie a resposta usando make_response
            response = make_response(url)

            # Defina o tipo MIME como application/pdf
            response.headers["Content-Type"] = "application/pdf"
            return url

        except Exception as e:
            abort(500, description=str(e))


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
