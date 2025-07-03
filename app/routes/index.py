import os
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from quart import (
    Blueprint,
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from quart_auth import login_required
from sqlalchemy import LargeBinary
from werkzeug.utils import secure_filename

from app import app
from app.forms import ImporteLotesForm
from app.misc import get_models

index = Blueprint("index", __name__)


@index.route("/termos_uso", methods=["GET"])
async def termos_uso() -> Response:
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
        # Crie a resposta usando make_response
        response = await make_response(
            await send_from_directory(app.config["PDF_PATH"], filename)
        )

        # Defina o tipo MIME como application/pdf
        response.headers["Content-Type"] = "application/pdf"
        return response

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@index.route("/politica_privacidade", methods=["GET"])
async def politica_privacidade() -> Response:
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

        # Crie a resposta usando make_response
        response = await make_response(
            send_from_directory(app.config["PDF_PATH"], filename)
        )

        # Defina o tipo MIME como application/pdf
        response.headers["Content-Type"] = "application/pdf"
        return response

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@index.route("/gen_relatorio")
@login_required
async def gen_relatorio() -> Response:
    try:
        referrer = (
            request.referrer.replace("http://", "").replace("https://", "").split("/")
        )
        referrer.remove(request.host)
        if "?" in referrer[-1]:
            chk_login = referrer[-1].split("?")[0]
            if chk_login == "login":
                return await make_response(redirect(url_for("dash.dashboard")))

        modelo = {
            "categorias": "categorias",
            "equipamentos": "equipamentos",
            "grades": "grades",
            "estoque_produto": "estoque_produto",
            "estoque_grade": "estoque_grade",
            "estoque_entradas": "estoque_entradas",
            "estoque_cautelas": "estoque_cautelas",
            "funcionarios": "funcionarios",
            "empresas": "empresas",
            "departamentos": "departamentos",
            "cargos": "cargos",
            "users": "users",
            "groups": "groups",
        }

        dbase = modelo.get(
            "_".join(referrer).lower()
            if "estoque" in referrer
            else referrer[-1].lower()
        )

        if not dbase:
            raise ValueError("Not Found!")

        filename = secure_filename(
            "".join(
                (
                    f"Relatório {' '.join([i.capitalize() for i in dbase.split('_')])}",
                    " - ",
                    f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.xlsx",
                )
            )
        )
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        file_path = Path(
            os.path.normpath(
                Path(app.config["CSV_TEMP_PATH"]).joinpath(filename).resolve()
            )
        ).resolve()

        model = get_models(dbase.lower())
        query = db.session.query(model).all()

        data = [
            {
                k: v
                for k, v in item.__dict__.items()
                if k != "_sa_instance_state"
                and not isinstance(item.__table__.columns[k].type, LargeBinary)
                and k != "filename"
            }
            for item in query
        ]

        df = pd.DataFrame(data)

        df.to_excel(file_path, index=False)

        response = await make_response(
            await send_file(
                file_path,
                as_attachment=True,
                cache_timeout=1,
            )
        )
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@index.route("/import_lotes/<tipo>", methods=["GET", "POST"])
@login_required
async def import_lotes(tipo: str = None) -> Response:
    try:
        action = request.path

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = ImporteLotesForm()

        model = get_models(tipo.lower())
        if form.validate_on_submit():
            doc = form.arquivo.raw_data[0]

            docname = secure_filename(doc.filename)
            doc.save(os.path.join(app.config["CSV_TEMP_PATH"], f"{docname}"))
            doc_path = os.path.join(app.config["CSV_TEMP_PATH"], f"{docname}")

            df = pd.read_excel(doc_path)
            df.columns = df.columns.str.lower()

            try:
                data_admissao = df["data_admissao"]
            except Exception:
                data_admissao = None

            if data_admissao is not None:
                df["data_admissao"] = pd.to_datetime(
                    df["data_admissao"], errors="coerce"
                )

            data = []
            for _, row in df.iterrows():
                row = row.dropna()
                data_info = row.to_dict()

                appends = model(**data_info)
                data.append(appends)

            if tipo.lower() == "grade":
                data = []
                for _, row in df.iterrows():
                    data_info = row.to_dict()
                    d = data_info.get("grade")

                    check_entry = model.query.filter_by(grade=d).first()

                    if not check_entry:
                        data_info.update({"grade": str(d)})
                        appends = model(**data_info)
                        data.append(appends)

            db.session.add_all(data)
            db.session.commit()

            await flash("Informação cadastrada com sucesso!", "success")
            return await make_response(redirect(url_for(tipo)))

        return await make_response(
            await render_template(
                "forms/importform.html", form=form, action=action, model=tipo
            )
        )

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)


@index.route("/gen_model/<model>", methods=["GET"])
@login_required
async def gen_model(model: str) -> Response:
    try:
        database_model = get_models(model.lower())

        columns = {}

        columns.update(database_model.__dict__)

        name_list = [i.capitalize() for i in model.split("_")]
        name_list.append(datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))

        str_model = " ".join(name_list)

        to_filter = list(columns.keys())
        for key in to_filter:
            if (
                key.startswith("_")
                or key == "filename"
                or key == "blob_doc"
                or key == "id"
            ):
                columns.pop(key)
                continue

            columns.update({key: ""})

        # Criando um DataFrame com as colunas
        df = pd.DataFrame(data=[columns])

        # Salvando o DataFrame em uma planilha
        filename = f"{str_model}.xlsx"
        file_path = os.path.join(app.config["TEMP_PATH"], filename)

        with pd.ExcelWriter(file_path, engine="auto") as writer:
            df.to_excel(writer, index=False, sheet_name="Sheet1")

        response = await make_response(
            await send_file(f"{file_path}", as_attachment=True)
        )
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        app.logger.exception(traceback.format_exception(e))
        abort(500)
