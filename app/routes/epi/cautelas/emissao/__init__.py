import json
import os
import shutil
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from time import sleep

from flask_sqlalchemy import SQLAlchemy
from quart import (
    Response,
    abort,
    current_app,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from app.decorators import create_perm
from app.forms import Cautela
from app.misc import (
    add_watermark,
    adjust_image_transparency,
    create_EPI_control_sheet,
    create_watermark_pdf,
)
from app.models import (
    Funcionarios,
    RegistrosEPI,
)
from app.routes.epi import estoque_bp
from app.routes.epi.cautelas.actions import employee_info
from app.routes.epi.cautelas.emissao.substract import subtract_estoque

from . import form_manipulation

__all__ = ["form_manipulation"]


@estoque_bp.route("/emitir_cautela", methods=["GET", "POST"])
@login_required
@create_perm
async def emitir_cautela() -> Response:
    try:
        form = Cautela()
        page = "forms/cautela/cautela_form.html"

        title = "Emissão de Cautela"
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if request.method == "POST":
            form_data2 = await request.form
            form = Cautela(
                choices_grade=[(form_data2["tipo_grade"], form_data2["tipo_grade"])]
            )

        if form.validate_on_submit():
            logo_empresa_path, funcionario = await employee_info(form, db)
            nomefilename = f"Cautela - {funcionario.nome_funcionario} - {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.pdf"

            return await emit_doc(
                db,
                funcionario,
                logo_empresa_path,
                await subtract_estoque(form, db, nomefilename),
                nomefilename,
            )

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        current_app.logger.error("\n".join(traceback.format_exception(e)))
        code = getattr(e, "code", 500)
        description = getattr(e, "description", "Internal Error")
        abort(code, description=description)


async def emit_doc(
    db: SQLAlchemy,
    data_funcionario: Funcionarios,
    logo_empresa_path: Path,
    list_epis_solict: list,
    nomefilename: str,
) -> Response:
    count_ = db.session.query(RegistrosEPI).all()
    year = datetime.now().year
    cod_lancamento = "".join((str(len(count_)).zfill(6), "-", str(year)))

    employee_data = {
        "company": str(data_funcionario.empresa),
        "name": str(data_funcionario.nome_funcionario),
        "cargo": str(data_funcionario.cargo),
        "departamento": str(data_funcionario.departamento),
        "registration": str(data_funcionario.codigo).zfill(6),
        "lancamento_code": cod_lancamento,
    }

    item_data = [
        ["Descrição", "Qtde", "Grade", "CA"],
    ]

    for obj in list_epis_solict:
        item_data.append(obj)

    num = str(uuid.uuid4())

    adjusted_path = os.path.join(app.config["DOCS_PATH"], f"GuardEPI_adjusted{num}.png")
    temp_watermark_pdf = os.path.join(app.config["DOCS_PATH"], f"{num} marca_dagua.pdf")

    try:
        path_cautela = os.path.join(app.config["DOCS_PATH"], nomefilename)

        ctrl_sheet = os.path.join(
            app.config["DOCS_PATH"], f"EPI_control_sheet{num}.pdf"
        )

        adjust_image_transparency(str(logo_empresa_path), adjusted_path, 1)
        create_EPI_control_sheet(
            ctrl_sheet,
            employee_data,
            item_data=item_data,
            logo_path=adjusted_path,
        )
        create_watermark_pdf(adjusted_path, temp_watermark_pdf)
        add_watermark(ctrl_sheet, path_cautela, temp_watermark_pdf)

        sleep(2)

        set_cautela = RegistrosEPI.query.filter_by(filename=nomefilename).first()

        if set_cautela is None:
            abort(400, description="Erro ao emitir a Cautela!")

        with open(path_cautela, "rb") as file:
            cautela_data = file.read()
            set_cautela.blob_doc = cautela_data
            db.session.commit()

        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json"
        )
        json_obj = json.dumps([])

        with open(pathj, "w") as f:
            f.write(json_obj)

        folder_to_show = str(uuid.uuid4())
        path_toshow = Path(path_cautela).parent.resolve().joinpath(folder_to_show)
        path_toshow.mkdir(exist_ok=True)
        str_foldertoshow = str(path_toshow.joinpath(nomefilename))
        shutil.copy(path_cautela, str_foldertoshow)

        return await make_response(
            redirect(url_for("estoque.cautelas", to_show=folder_to_show))
        )

    except Exception as e:
        raise e
