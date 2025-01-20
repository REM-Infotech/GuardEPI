from flask import Flask, Response, make_response, redirect, render_template, url_for
from werkzeug.exceptions import HTTPException

from .auth import auth
from .config import config
from .corporativo import corp
from .dashboard import dash
from .epi import epi, estoque_bp
from .index import index as ind
from .serving import serve


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
        if error.code == 500 and "já cadastrado" not in error.desc:
            desc: str = "Erro do sistema"

        if error.code == 405:
            return make_response(redirect(url_for("dash.dashboard")))

        return make_response(
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
