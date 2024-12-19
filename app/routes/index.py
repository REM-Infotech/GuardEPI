from datetime import datetime
import os
from typing import Union
from flask import (
    Blueprint,
    current_app as app,
    make_response,
    render_template,
    send_file,
    send_from_directory,
    redirect,
    url_for,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from flask_login import login_required
import pandas as pd
from sqlalchemy import LargeBinary
from werkzeug.exceptions import HTTPException
from deep_translator import GoogleTranslator

from ..models import RegistrosEPI
from ..models import GradeEPI, ProdutoEPI
from ..models import EstoqueEPI, EstoqueGrade, RegistroEntradas
from ..models import Cargos, Departamento, Empresa, Funcionarios
from ..models.users import Groups, Users

epi_models = Union[
    RegistrosEPI,
    RegistroEntradas,
    EstoqueEPI,
    EstoqueGrade,
    GradeEPI,
    ProdutoEPI,
    Cargos,
    Departamento,
    Empresa,
    Funcionarios,
    Groups,
    Users,
]

index = Blueprint("index", __name__)


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


@index.route("/termos_uso", methods=["GET"])
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


@index.route("/politica_privacidade", methods=["GET"])
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


def get_models(tipo: str):
    models: dict[str, epi_models] = {
        "equipamentos": ProdutoEPI,
        "grades": GradeEPI,
        "estoque": EstoqueEPI,
        "estoque_grade": EstoqueGrade,
        "entradas": RegistroEntradas,
        "cautelas": RegistrosEPI,
        "funcionarios": Funcionarios,
        "empresas": Empresa,
        "departamentos": Departamento,
        "cargo.cargos": Cargos,
        "users": Users,
        "groups": Groups,
    }

    return models[tipo]


@app.route("/gerar_relatorio/<str:dbase>")
@login_required
def gerar_relatorio(dbase: str):
    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # Change colon to hyphen
        filename = f"Relatório {dbase.capitalize()} - {now}.xlsx"
        file_path = os.path.join(app.config["CSV_TEMP_PATH"], filename)

        model = get_models(dbase.lower())
        query = db.session.query(model).all()

        data = [
            {
                k: v
                for k, v in item.__dict__.items()
                if k != "_sa_instance_state"
                and not isinstance(item.__table__.columns[k].type, LargeBinary)
            }
            for item in query
        ]

        df = pd.DataFrame(data)

        df.to_excel(file_path, index=False)

        response = make_response(send_file(f"{file_path}", as_attachment=True))
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        abort(500, description=str(e))
