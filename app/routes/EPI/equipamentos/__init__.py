from datetime import datetime
from pathlib import Path
from typing import Union

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.decorators import set_endpoint
from app.forms import CadastroEPIForm
from app.misc import format_currency_brl
from app.models import ProdutoEPI

form_content = Union[str, FileStorage, int, float, datetime]

template_folder = Path(__file__).parent.resolve().joinpath("templates")
equip = Blueprint("equip", __name__, template_folder=template_folder)


@equip.route("/equipamentos")
@login_required
@set_endpoint
def Equipamentos():

    page = "equipamentos.html"
    title = request.endpoint.split(".")[1].capitalize()
    database = ProdutoEPI.query.all()
    DataTables = "js/DataTables/epi/EquipamentosTable.js"
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        format_currency_brl=format_currency_brl,
        DataTables=DataTables,
        url_image=url,
    )


@equip.route("/equipamentos/cadastro", methods=["GET", "POST"])
@login_required
def cadastro():

    form = CadastroEPIForm()

    if form.validate_on_submit():
        db: SQLAlchemy = app.extensions["sqlalchemy"]
        to_add = {}

        form_data: dict[str, form_content] = list(form.data.items())
        for key, value in form_data:
            if key == "csrf_token":
                continue

            if key == "submit":
                continue

            if key == "valor_unitario":
                value = float(
                    value.replace(",", ".").replace("R$", "").replace(" ", "")
                )

            if isinstance(value, FileStorage):
                filename = secure_filename(value.filename)
                path_file = Path(app.config.get("TEMP_PATH")).joinpath(filename)
                value.save(str(path_file))
                with path_file.open("rb") as file:
                    to_add.update({"blob_doc": file.read()})

                to_add.update({"filename": filename})
                continue

            to_add.update({key: value})

        epi = ProdutoEPI(**to_add)
        db.session.add(epi)
        db.session.commit()

        flash("EPI cadastrado com sucesso!", "success")
        return redirect(url_for("equip.Equipamentos"))

    page = "form.html"
    return render_template("index.html", page=page, form=form)


@equip.route("/equipamentos/editar/<id>", methods=["GET", "POST"])
@login_required
def editar(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    epi = db.session.query(ProdutoEPI).filter_by(id=id).first()

    form_data = {}

    form = CadastroEPIForm()

    if request.method == "GET":

        url_image = ""
        epi_data = epi.__dict__

        items_epi_data = list(epi_data.items())

        for key, value in items_epi_data:

            if key == "_sa_instance_state" or key == "id" or key == "filename":

                continue

            if key == "blob_doc":

                img_path = (
                    Path(app.config.get("TEMP_PATH"))
                    .joinpath("IMG")
                    .joinpath(epi_data.get("filename"))
                )
                with img_path.open("wb") as file:
                    file.write(value)

                with img_path.open("rb") as file:
                    form_data.update(
                        {
                            "filename": FileStorage(
                                filename=secure_filename(epi.filename),
                                stream=file.read(),
                            )
                        }
                    )

                    url_image = url_for(
                        "serve.serve_img", filename=epi.filename, _external=True
                    )

            if key == "valor_unitario":
                value = format_currency_brl(value).replace("\\xa", "")

            form_data.update({key: value})

        form = CadastroEPIForm(**form_data)

    if form.validate_on_submit():

        to_add = {}

        form_data: dict[str, form_content] = list(form.data.items())
        for key, value in form_data:

            if value:
                if key == "csrf_token":
                    continue

                if key == "submit":
                    continue

                if key == "valor_unitario":
                    value = float(
                        value.replace(",", ".").replace("R$", "").replace(" ", "")
                    )

                if isinstance(value, FileStorage):
                    filename = secure_filename(value.filename)
                    path_file = Path(app.config.get("TEMP_PATH")).joinpath(filename)
                    value.save(str(path_file))
                    with path_file.open("rb") as file:
                        to_add.update({"blob_doc": file.read()})

                    to_add.update({"filename": filename})
                    continue

                setattr(epi, key, value)

        db.session.commit()

        flash("Edições Salvas con sucesso!", "success")
        return redirect(url_for("equip.Equipamentos"))

    page = "form.html"
    return render_template("index.html", page=page, form=form, url_image=url_image)
