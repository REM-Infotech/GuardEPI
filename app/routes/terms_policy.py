from flask import abort, make_response, send_from_directory

from app import app


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
