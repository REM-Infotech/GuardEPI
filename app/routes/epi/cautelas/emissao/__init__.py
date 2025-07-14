import json
import os
import shutil
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from time import sleep

import aiofiles
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
from app.routes.epi.cautelas.actions.employee import employee_info
from app.routes.epi.cautelas.actions.saida import RegistrarSaida

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
            arquivo_cautela = f"Cautela - {funcionario.nome_funcionario} - {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.pdf"
            epis_solicitadas = await RegistrarSaida(form, db, arquivo_cautela)()
            return await emitir_documento(
                db,
                funcionario,
                logo_empresa_path,
                epis_solicitadas,
                arquivo_cautela,
            )

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        current_app.logger.error("\n".join(traceback.format_exception(e)))
        code = getattr(e, "code", 500)
        description = getattr(e, "description", "Internal Error")
        abort(code, description=description)


async def emitir_documento(
    db: SQLAlchemy,
    data_funcionario: Funcionarios,
    logo_empresa_path: Path,
    epis_solicitadas: list[str],
    arquivo_cautela: str,
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

    item_data.extend([epi for epi in epis_solicitadas])

    num = str(uuid.uuid4())

    docs_path = Path(app.config["DOCS_PATH"]).resolve()

    adjusted_path = os.path.join(docs_path, f"GuardEPI_adjusted{num}.png")
    temp_watermark_pdf = os.path.join(docs_path, f"{num} marca_dagua.pdf")
    path_cautela = os.path.join(docs_path, arquivo_cautela)

    try:
        ctrl_sheet = os.path.join(docs_path, f"EPI_control_sheet{num}.pdf")

        adjust_image_transparency(str(logo_empresa_path), adjusted_path, 1)
        create_EPI_control_sheet(ctrl_sheet, employee_data, item_data, adjusted_path)
        create_watermark_pdf(adjusted_path, temp_watermark_pdf)
        add_watermark(ctrl_sheet, path_cautela, temp_watermark_pdf)

        sleep(2)

        set_cautela = (
            db.session.query(RegistrosEPI).filter_by(filename=arquivo_cautela).first()
        )

        if set_cautela is None:
            abort(400, description="Erro ao emitir a Cautela!")

        async with aiofiles.open(path_cautela, "rb") as file:
            cautela_data = await file.read()
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
        str_foldertoshow = str(path_toshow.joinpath(arquivo_cautela))
        shutil.copy(path_cautela, str_foldertoshow)

        return await make_response(
            redirect(url_for("estoque.cautelas", to_show=folder_to_show))
        )

    except Exception as e:
        raise e
