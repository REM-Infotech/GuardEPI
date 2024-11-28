import os
from datetime import datetime
from typing import Type

import requests
from dotenv import dotenv_values
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.decorators import create_perm, read_perm, set_endpoint
from app.Forms import (
    CadastroClasses,
    CadastroEPIForm,
    CadastroFonecedores,
    CadastroMarcas,
    CadastroModelos,
    EditItemProdutoForm,
    IMPORTEPIForm,
)
from app.misc import format_currency_brl
from app.models import ClassesEPI
from app.models import Fornecedores as fornecedores
from app.models import Marcas as marcas
from app.models import ModelosEPI, ProdutoEPI

tipo = db.Model


def get_models(tipo) -> Type[tipo]:

    models = {
        "equipamentos": ProdutoEPI,
        "fornecedores": fornecedores,
        "marcas": marcas,
        "modelos": ModelosEPI,
        "classes": ClassesEPI,
    }

    return models[tipo]


@app.route("/Equipamentos")
@login_required
@set_endpoint
@read_perm
def Equipamentos():

    importForm = IMPORTEPIForm()
    form = CadastroEPIForm()
    page = f"pages/epi/{request.endpoint.lower()}.html"
    title = request.endpoint.capitalize()
    database = get_models(request.endpoint.lower()).query.all()
    DataTables = "js/DataTables/epi/EquipamentosTable.js"
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return render_template(
        "index.html",
        page=page,
        title=title,
        form=form,
        importForm=importForm,
        database=database,
        format_currency_brl=format_currency_brl,
        DataTables=DataTables,
        url_image=url,
    )


@app.route("/SetEditarEPI/<item>", methods=["GET"])
@login_required
def SetEditarEPI(item: int):

    form = EditItemProdutoForm
    model = ProdutoEPI
    database = model.query.filter(model.id == item).first()
    route = request.referrer.replace("https://", "").replace("http://", "")
    route = route.split("/")[1].lower()

    if "?" in route:
        route = route.split("?")[0]

    form = form(
        **{
            "nome_epi": database.nome_epi,
            "ca": database.ca,
            "cod_ca": database.cod_ca,
            "valor_unitario": format_currency_brl(database.valor_unitario),
            "periodicidade_item": database.periodicidade_item,
            "qtd_entregar": database.qtd_entregar,
            "fornecedor": database.fornecedor,
            "marca": database.marca,
            "modelo": database.modelo,
            "tipo_epi": database.tipo_epi,
            "vencimento": database.vencimento,
            "descricao": database.descricao,
            "filename": database.filename,
        }
    )

    url = ""
    if any(route == tipos for tipos in ["empresas", "equipamentos"]):

        image_name = database.filename
        url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
        form.filename.data = url
        if image_name:
            url = url_for(
                "serve_img", index=item, md=route, _external=True, _scheme="https"
            )

    grade_results = f"pages/forms/{route}/edit.html"
    return render_template(grade_results, form=form, url=url, tipo=route, id=item)


@app.route("/cadastrarEPI", methods=["POST"])
@login_required
@create_perm
def cadastrarEPI():

    form = CadastroEPIForm()

    if form.validate_on_submit():

        dbase_tipoepi = ClassesEPI.query.filter(
            ClassesEPI.classe == form.tipo_epi.data
        ).first()

        args = dotenv_values()

        username = args.get("username_api", None)
        password = args.get("password_api", None)

        url = args.get("url_api", None)

        if username and password and url:
            auth = {"username": username, "password": password}

            data = requests.post(f"{url}/login", json=auth).json()

            headers = {"Authorization": f"Bearer {data.get('access_token')}"}

            # Faça a requisição GET (ou POST, PUT, etc.) com o cabeçalho
            url_request = f"{url}/consulta_ca/{form.data.get("cod_ca", "99999")}"
            response = requests.get(url_request, headers=headers)

            if response.status_code == 200:

                response = response.json()

                # Formato da string de data
                date_format = "%a, %d %b %Y %H:%M:%S %Z"

                # Converter para datetime
                response.update(
                    {
                        "validade": datetime.strptime(
                            response.get("validade"), date_format
                        )
                    }
                )

                form.tipo_epi.data = response["tipo_epi"]
                form.vencimento.data = response["validade"]
                form.descricao.data = response["aprovado_para"]

        if not dbase_tipoepi:

            addClasse = ClassesEPI(classe=response["tipo_epi"])

            db.session.add(addClasse)

        if "R$" in str(form.valor_unitario.data):
            form.valor_unitario.data = float(
                str(form.valor_unitario.data)
                .replace("R$ ", "")
                .replace(".", "")
                .replace(",", ".")
            )

        epi_insert = ProdutoEPI(
            ca=form.ca.data,
            cod_ca=form.cod_ca.data,
            nome_epi=form.nome_epi.data,
            tipo_epi=form.tipo_epi.data,
            valor_unitario=form.valor_unitario.data,
            qtd_entregar=form.qtd_entregar.data,
            periodicidade_item=form.periodicidade_item.data,
            fornecedor=form.fornecedor.data,
            marca=form.marca.data,
            modelo=form.modelo.data,
            vencimento=form.vencimento.data,
            descricao=form.descricao.data,
        )

        if form.filename.data:

            img_epi = form.filename.data

            filename = secure_filename(img_epi.filename)
            path_img = os.path.join(app.config["IMAGE_TEMP_PATH"], filename)
            img_epi.save(path_img)
            with open(path_img, "rb") as f:
                img_data = f.read()

            epi_insert.filename = filename
            epi_insert.blob_doc = img_data

        db.session.add(epi_insert)
        db.session.commit()

        flash("Informações salvas com sucesso!", "success")
        return redirect(url_for("Equipamentos"))

    if form.errors:
        pass

    return redirect(url_for("Equipamentos"))


@app.route("/Fornecedores", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Fornecedores():

    form = CadastroFonecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@app.route("/Marcas", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Marcas():

    form = CadastroMarcas()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@app.route("/Modelos", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Modelos():

    form = CadastroModelos()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@app.route("/Classes", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Classes():

    form = CadastroClasses()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
