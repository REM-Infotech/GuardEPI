import json
import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import List

from flask_sqlalchemy import SQLAlchemy
from quart import (
    Response,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from ....decorators import create_perm
from ....forms import Cautela
from ....misc import (
    add_watermark,
    adjust_image_transparency,
    create_EPI_control_sheet,
    create_watermark_pdf,
)
from ....models import (
    Empresa,
    EPIsCautela,
    EstoqueEPI,
    EstoqueGrade,
    Funcionarios,
    ProdutoEPI,
    RegistroSaidas,
    RegistrosEPI,
)
from .. import estoque_bp


@estoque_bp.before_request
async def setgroups() -> None:
    if request.endpoint == "estoque.emitir_cautela" and request.method == "GET":
        session["uuid_Cautelas"] = str(uuid.uuid4())
        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json"
        )

        if os.path.exists(pathj):
            os.remove(pathj)

        json_obj = json.dumps([])

        with open(pathj, "w") as f:
            f.write(json_obj)


@estoque_bp.route("/add_itens", methods=["GET", "POST"])
@login_required
@create_perm
async def add_itens() -> Response:
    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        form = Cautela()

        nome_epi = form.nome_epi.data
        grade_epi = form.tipo_grade.data

        item_cautela = {
            "NOME_EPI": nome_epi,
            "GRADE": form.tipo_grade.data,
            "QTD": form.qtd_entregar.data,
        }

        data_estoque = (
            db.session.query(EstoqueEPI).filter(EstoqueEPI.nome_epi == nome_epi).first()
        )
        estoque_grade = (
            db.session.query(EstoqueGrade)
            .filter(
                EstoqueGrade.nome_epi == nome_epi,
                EstoqueGrade.grade == grade_epi,
            )
            .first()
        )

        if estoque_grade is not None:
            if all([estoque_grade.qtd_estoque == 0, data_estoque.qtd_estoque == 0]):
                return await make_response(
                    render_template("forms/cautela/not_estoque.html", epi_name=nome_epi)
                )

        elif estoque_grade is None:
            return await make_response(
                render_template(
                    "forms/cautela/not_estoque.html",
                    message="EPI não registrada no estoque!",
                )
            )

        pathj = os.path.join(
            app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json"
        )

        with open(pathj, "rb") as f:
            list_epis: list[dict[str, str | int]] = json.load(f)

        item_cautela.update({"ID": len(list_epis)})

        list_epis.append(item_cautela)
        json_obj = json.dumps(list_epis)

        with open(pathj, "w") as f:
            f.write(json_obj)

        item_html = render_template("forms/cautela/add_items.html", item=list_epis)

        # Retorna o HTML do item
        return await make_response(item_html)
    except Exception as e:
        abort(500, description=str(e))


@estoque_bp.route("/remove-itens", methods=["GET", "POST"])
@login_required
@create_perm
async def remove_itens() -> Response:
    pathj = os.path.join(app.config["TEMP_PATH"], f"{session['uuid_Cautelas']}.json")
    json_obj = json.dumps([])

    with open(pathj, "w") as f:
        f.write(json_obj)

    item_html = render_template("forms/cautela/add_items.html")
    return await make_response(item_html)


@estoque_bp.post("/get_grade")
@login_required
@create_perm
async def get_grade() -> Response:
    try:
        form = Cautela()
        lista = []
        dbase = EstoqueGrade.query.filter_by(nome_epi=form.nome_epi.data).all()
        for query in dbase:
            lista.append((query.grade, query.grade))
        form.tipo_grade.choices.extend(lista)

        page = "forms/cautela/get_grade.html"
        return await make_response(render_template(page, form=form))
    except Exception as e:
        abort(500, description=str(e))


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
            form_data2 = request.form
            form = Cautela(
                choices_grade=[(form_data2["tipo_grade"], form_data2["tipo_grade"])]
            )

        if form.validate_on_submit():
            logo_empresa_path, funcionario = employee_info(form, db)
            nomefilename = f"Cautela - {funcionario.nome_funcionario} - {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.pdf"

            return emit_doc(
                db,
                funcionario,
                logo_empresa_path,
                subtract_estoque(form, db, nomefilename),
                nomefilename,
            )

        return await make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception as e:
        code = getattr(e, "code", 500)
        description = getattr(e, "description", "Internal Error")
        abort(code, description=description)


async def subtract_estoque(form: Cautela, db: SQLAlchemy, nomefilename: str) -> list:
    try:
        epis_lista = []
        para_registro = []
        list_epis_solict = []

        path_json = Path(app.config["TEMP_PATH"]).joinpath(
            f"{session['uuid_Cautelas']}.json"
        )

        with path_json.open("rb") as f:
            list_epis: list = json.load(f)

        if len(list_epis) == 0:
            raise ValueError("Adicione ao menos 1a EPI!")

        for item_epi in list_epis:
            nome_epi = item_epi.get("NOME_EPI")
            grade_epi = item_epi.get("GRADE")
            qtd_entrega = item_epi.get("QTD")
            if nome_epi is None:
                continue

            equip = (
                db.session.query(ProdutoEPI)
                .filter(ProdutoEPI.nome_epi == nome_epi)
                .first()
            )

            data_estoque = (
                db.session.query(EstoqueEPI)
                .filter(EstoqueEPI.nome_epi == nome_epi)
                .first()
            )
            estoque_grade = (
                db.session.query(EstoqueGrade)
                .filter(
                    EstoqueGrade.nome_epi == nome_epi,
                    EstoqueGrade.grade == grade_epi,
                )
                .first()
            )

            if estoque_grade:
                if all([estoque_grade.qtd_estoque > 0, data_estoque.qtd_estoque > 0]):
                    list_epis_solict.append(
                        [str(nome_epi), qtd_entrega, grade_epi, equip.ca]
                    )
                    epis_lista.append(equip)
                    para_registro.append(
                        RegistroSaidas(
                            nome_epi=nome_epi,
                            qtd_saida=int(qtd_entrega),
                            valor_total=equip.valor_unitario * int(qtd_entrega),
                        )
                    )

                    estoque_grade.qtd_estoque -= 1
                    data_estoque.qtd_estoque -= 1
                    valor_calc = equip.valor_unitario * int(qtd_entrega)

        funcionario = form.funcionario.data

        registrar = RegistrosEPI(
            funcionario=funcionario,
            data_solicitacao=datetime.now(),
            filename=nomefilename,
            valor_total=valor_calc,
        )

        registrar.nome_epis = (
            json.dumps(para_registro).replace("[", "").replace("]", "")
        )

        secondary: List[EPIsCautela] = []
        for epi in para_registro:
            registro_secondary = EPIsCautela(cod_ref=str(uuid.uuid4()))
            registro_secondary.epis_saidas = epi
            registro_secondary.nome_epis = registrar
            secondary.append(registro_secondary)

        db.session.add(registrar)
        db.session.add_all(secondary)
        db.session.add_all(para_registro)
        db.session.commit()

        return list_epis_solict

    except Exception as e:
        raise e


async def employee_info(
    form: Cautela, db: SQLAlchemy
) -> tuple[Path, Funcionarios | None]:
    funcionario_data = (
        db.session.query(Funcionarios)
        .filter(Funcionarios.nome_funcionario == form.funcionario.data)
        .first()
    )

    nome_empresa = funcionario_data.empresa
    empresa_data = (
        db.session.query(Empresa).filter(Empresa.nome_empresa == nome_empresa).first()
    )
    image_data = empresa_data.blob_doc
    original_path = Path(app.config["IMAGE_TEMP_PATH"]).joinpath(empresa_data.filename)

    with original_path.open("wb") as f:
        f.write(image_data)

    return original_path, funcionario_data


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
