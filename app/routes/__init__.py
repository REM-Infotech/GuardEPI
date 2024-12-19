from flask import (
    Flask,
)

from .auth import auth
from .corporativo import corp
from .dashboard import dash
from .epi import epi
from .serving import serve
from .index import index as ind


def register_routes(app: Flask):
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

    with app.app_context():

        blueprints = [auth, dash, corp, epi, serve, ind]

        for blueprint in blueprints:
            app.register_blueprint(blueprint)


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
