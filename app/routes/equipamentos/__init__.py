from pathlib import Path

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import (
    CadastroCategorias,
    CadastroEPIForm,
    CadastroFornecedores,
    Cadastromarcas,
    CadastroModelos,
    IMPORTEPIForm,
)
from app.misc import format_currency_brl
from app.models import get_models

template_folder = Path(__file__).joinpath("templates")
equip = Blueprint("equip", __name__, template_folder=template_folder)


@equip.route("/equipamentos")
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


@equip.route("/fornecedores", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def fornecedores():

    form = CadastroFornecedores()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@equip.route("/marcas", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def marcas():

    form = Cadastromarcas()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@equip.route("/modelos", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def modelos():

    form = CadastroModelos()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )


@equip.route("/categorias", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def categorias():

    form = CadastroCategorias()
    DataTables = "js/DataTables/DataTables.js"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = get_models(request.endpoint.lower()).query.all()
    return render_template(
        "index.html", page=page, form=form, DataTables=DataTables, database=database
    )
