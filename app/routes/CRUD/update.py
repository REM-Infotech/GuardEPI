from flask_login import login_required
from flask import (
    redirect,
    url_for,
    render_template,
    session,
    abort,
    flash,
    send_from_directory,
)
from flask_wtf import FlaskForm

from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from wtforms import DateField
from sqlalchemy import LargeBinary
from sqlalchemy import Float

from app.decorators import update_perm
from app.misc import format_currency_brl, generate_pid
from app.models.EPI import ProdutoEPI, GradeEPI, RegistrosEPI
from app.models.Funcionários import Empresa, Funcionarios, Cargos, Departamento
from app.Forms.edit import (
    EditItemProdutoForm,
    EditSaldoGrade,
    EditFuncionario,
    EditEmpresa,
    EditDepartamentos,
    EditCargo,
)
from app import app
from app import db

import os
from typing import Type
from datetime import datetime
import requests

tipo = db.Model


def getform(form) -> Type[FlaskForm]:

    forms = {
        "edit_equipamentos": EditItemProdutoForm(),
        "edit_estoque": EditSaldoGrade(),
        "edit_funcionarios": EditFuncionario(),
        "edit_empresas": EditEmpresa(),
        "edit_departamentos": EditDepartamentos(),
        "edit_cargos": EditCargo(),
    }

    return forms[form]


def get_models(tipo: str) -> Type[tipo]:

    models = {
        "equipamentos": ProdutoEPI,
        "estoque": GradeEPI,
        "empresas": Empresa,
        "funcionarios": Funcionarios,
        "departamentos": Departamento,
        "cargos": Cargos,
    }

    return models[tipo]


@app.route("/set_editar/<tipo>/<item>", methods=["GET"])
@login_required
def set_editar(tipo: str, item: int):

    tipo = tipo.lower()
    session["item_edit"] = item
    form = getform(f"edit_{tipo}")
    model = get_models(tipo.replace("edit_", ""))
    database = model.query.filter(model.id == item).all()
    colunas = []
    for i in model.__table__.columns:

        if isinstance(i.type, LargeBinary):
            continue
        name = getattr(i, "name")
        colunas.append(name)

    for itens in database:
        for i in colunas:
            for column in itens.__table__.columns:
                if isinstance(column.type, LargeBinary):
                    form_field = getattr(form, f"{column.name.lower()}", None)
                    if form_field:
                        set_data = getattr(itens, column.name)
                if i == column.name:
                    form_field = getattr(form, f"{column.name.lower()}", None)
                    if form_field:
                        set_data = getattr(itens, column.name)
                        if isinstance(column.type, Float):
                            set_data = format_currency_brl(set_data)

                        if isinstance(form_field, DateField):
                            set_data = datetime.strptime(
                                set_data.strftime("%d-%m-%Y"), "%d-%m-%Y"
                            ).date()
                            form_field.data = set_data

                        if not form_field.data:
                            form_field.data = set_data
        break

    url = ""
    if any(tipo == tipos for tipos in ["empresas", "equipamentos"]):

        image_name = form.imagem.data
        if image_name is None:

            url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
            form.imagem.data = url

        else:
            url = url_for(
                "serve_img",
                filename=image_name,
                model=tipo,
                _external=True,
                _scheme="https",
            )

    grade_results = f"pages/forms/{tipo}/edit.html"

    return render_template(grade_results, form=form, url=url, tipo=tipo, id=item)


@app.route("/editar/<tipo>/<id>", methods=["POST"])
@login_required
@update_perm
def editar(tipo: str | None, id: int):

    form = getform(f"edit_{tipo}")
    model = get_models(tipo)

    try:
        if form.validate_on_submit():

            kwargs = {}
            for i in model.__table__.columns:
                name = getattr(i, "name")
                kwargs[name] = ""

            itens = model.query.filter_by(id=int(id)).first()
            for i in kwargs:
                for column in itens.__table__.columns:
                    if i == column.name:
                        form_field = getattr(form, f"{column.name}", None)
                        if form_field:

                            data_insert = form_field.data
                            if data_insert is None:
                                if isinstance(form_field, FileField):
                                    file_column = column
                                continue

                            if isinstance(form_field, FileField):
                                file_column = column

                            if isinstance(data_insert, str) and "R$" in data_insert:

                                data_insert = form.valor_unitario.data.encode(
                                    "latin-1", "ignore"
                                ).decode("latin-1")
                                data_insert = (
                                    data_insert.replace(r"R$\xa", "")
                                    .replace("R$ ", "")
                                    .replace(".", "")
                                    .replace(",", ".")
                                )
                                data_insert = float(data_insert)
                            setattr(itens, column.name, data_insert)

                        if isinstance(column.type, LargeBinary):
                            for form_field in form:
                                if isinstance(form_field, FileField):
                                    file = form_field.data
                                    set_data = getattr(itens, column.name)
                                    if file:
                                        docname = secure_filename(file.filename)
                                        now = generate_pid()
                                        filename = f"{now}{docname}"
                                        path_img = os.path.join(
                                            app.config["IMAGE_TEMP_PATH"], filename
                                        )
                                        file.save(path_img)
                                        with open(path_img, "rb") as file:
                                            setattr(itens, column.name, file.read())
                                        setattr(itens, file_column.name, filename)
                                    elif set_data is None:
                                        image_url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
                                        img_data = requests.get(image_url)
                                        setattr(itens, column.name, img_data.content)
                                        cod = generate_pid()
                                        now = datetime.now().strftime("%d%m%Y%H%M%S")
                                        filename = f"{now}{cod}.png"
                                        setattr(itens, file_column.name, filename)
                                    break

            db.session.commit()
            flash("Edições salvas com sucesso!", "success")
            return redirect(f"/{tipo.capitalize()}")

        if form.errors:

            for erros in list(form.errors):
                message = form.errors[erros][0]
                flash(message, "error")

    except Exception as e:
        abort(500, description=str(e))


@app.route("/pdf/<index>", methods=["GET"])
@login_required
def serve_pdf(index):

    try:
        index = int(index)
        with app.app_context():

            dbase = RegistrosEPI.query.filter_by(id=index).first()
            filename = dbase.doc_cautela
            pdf_data = dbase.blob_cautela

            original_path = os.path.join(app.config["DOCS_PATH"], filename)

            with open(original_path, "wb") as file:
                file.write(pdf_data)
            url = send_from_directory(app.config["DOCS_PATH"], filename)

            return url

    except Exception as e:
        abort(500, description=str(e))


@app.route("/img/<filename>/<model>", methods=["GET"])
@login_required
def serve_img(filename: str, model: str):

    try:
        with app.app_context():

            dbase = get_models(model.lower())
            image_data = dbase.query.filter_by(imagem=filename).first()

            image_data = image_data.blob_imagem
            now = generate_pid()
            filename = f"{now}.png"
            original_path = os.path.join(app.config["IMAGE_TEMP_PATH"], filename)

            with open(original_path, "wb") as file:
                file.write(image_data)

            url = send_from_directory(app.config["IMAGE_TEMP_PATH"], filename)

            return url

    except Exception as e:
        abort(500, description=str(e))
