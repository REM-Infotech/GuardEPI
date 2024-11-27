from os import path
from pathlib import Path

from flask import Blueprint, abort, render_template, request
from flask_login import login_required

from app.decorators import read_perm, set_endpoint
from app.Forms.create import CadastroCargo
from app.Forms.globals import IMPORTEPIForm
from app.models.Funcionários import Cargos

template_folder = path.join(Path(__file__).parent.resolve(), "templates")
cargo_bp = Blueprint(
    "cargo_bp", __name__, template_folder=template_folder, static_folder="static"
)


@cargo_bp.route("/cargos")
@login_required
@set_endpoint
@read_perm
def cargos():

    try:
        importForm = IMPORTEPIForm()
        page = f"pages/Gestao/{request.endpoint.lower().split(".")[-1]}.html"
        database = Cargos.query.all()
        DataTables = f"js/DataTables/gestao/{request.endpoint.capitalize()}Table.js"
        form = CadastroCargo()
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
            DataTables=DataTables,
            importForm=importForm,
        )
    except Exception as e:
        abort(500, description=str(e))
