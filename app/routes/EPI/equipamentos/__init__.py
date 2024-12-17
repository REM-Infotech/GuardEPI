from pathlib import Path

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.forms import CadastroEPIForm, IMPORTEPIForm
from app.misc import format_currency_brl

template_folder = Path(__file__).parent.resolve().joinpath("templates")
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
    database = []
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
