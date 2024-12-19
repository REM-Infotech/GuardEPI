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
from .epi import epi
from .serving import serve


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
        """
        Handles HTTP exceptions by translating the error name to Portuguese and rendering an error template.
        Args:
            error (HTTPException): The HTTP exception that was raised.
        Returns:
            Response: A Flask response object with the rendered error template and the appropriate HTTP status code.
        """
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
        """
        Rota para servir o arquivo "Termos de Uso.pdf".

        Esta rota responde a requisições GET e retorna o arquivo PDF "Termos de Uso.pdf"
        localizado no diretório configurado em `app.config["PDF_PATH"]`.

        Returns:
            Response: Um objeto de resposta contendo o arquivo PDF e o cabeçalho de tipo MIME
            definido como "application/pdf".

        Raises:
            HTTPException: Retorna um erro 500 se ocorrer qualquer exceção durante o processo.
        """
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
        """
        Rota para servir o arquivo de Política de Privacidade em formato PDF.

        Tenta enviar o arquivo "Política de Privacidade.pdf" do diretório configurado em "PDF_PATH".
        Define o tipo MIME da resposta como "application/pdf".

        Returns:
            Response: A resposta contendo o arquivo PDF.

        Raises:
            HTTPException: Se ocorrer algum erro ao tentar enviar o arquivo, retorna um erro 500 com a descrição do erro.
        """
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
