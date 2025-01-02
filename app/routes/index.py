import os
from datetime import datetime

import pandas as pd
from flask import Blueprint, abort
from flask import current_app as app
from flask import (
    flash,
    make_response,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for,
)
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from werkzeug.utils import secure_filename

from app.forms import ImporteLotesForm
from app.misc import get_models

index = Blueprint("index", __name__)


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


@index.route("/gerar_relatorio/<dbase>")
@login_required
def gerar_relatorio(dbase: str):
    try:

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        referrer = (
            request.referrer.replace("http://", "").replace("https://", "").split("/")
        )

        referrer.remove(request.host)

        if "estoque" in referrer:
            dbase = "_".join(referrer)

        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # Change colon to hyphen
        filename = f"Relatório {" ".join([i.capitalize() for i in dbase.split("_")])} - {now}.xlsx"
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


@index.route("/import_lotes/<tipo>", methods=["GET", "POST"])
@login_required
def import_lotes(tipo: str = None):
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

            flash("Informação cadastrada com sucesso!", "success")
            return redirect(url_for(tipo))

        return render_template(
            "forms/importform.html", form=form, action=action, model=tipo
        )

    except Exception as e:
        abort(400, description=str(e))


@index.route("/gen_model/<model>", methods=["GET"])
@login_required
def gen_model(model: str):

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

        response = make_response(send_file(f"{file_path}", as_attachment=True))
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        abort(500, description=str(e))
