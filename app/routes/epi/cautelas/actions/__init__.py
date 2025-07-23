import shutil
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import TypedDict
from uuid import uuid4

import aiofiles
import camelot
import pytz
from flask_sqlalchemy import SQLAlchemy
from pandas import DataFrame
from quart import current_app as app
from quart.datastructures import FileStorage

from app.forms.epi import FormEnvioCautelaAssinada
from app.models.EPI.cautelas import (
    CautelaAssinada,
    RegistrosCautelasCanceladas,
    RegistrosEPI,
)
from app.models.EPI.estoque import EstoqueEPI, EstoqueGrade
from app.models.Funcionários import Funcionarios


class ItemCautela(TypedDict):
    DESCRICAO: str
    QTDE: str
    GRADE: str
    CA: str


async def cancelamento_cautela(db: SQLAlchemy, id_cautela: int):
    query = db.session.query(RegistrosEPI).filter_by(id=id_cautela).first()
    path_pdf = Path(app.config["DOCS_PATH"]).resolve()

    path_pdf = path_pdf.joinpath(query.filename)

    async with aiofiles.open(path_pdf, "wb") as f:
        await f.write(query.blob_doc)

    tables = camelot.read_pdf(path_pdf)
    dataframe: DataFrame = tables[-1].df
    data = dataframe.to_dict(orient="records")

    keys: list[dict[int, str]] = data[0]

    equips: list[ItemCautela] = []

    for item in data[1:]:
        desc = (
            str(keys[0]).replace("\n", "").replace("ç", "c").replace("ã", "a").upper()
        )
        equips.append(
            ItemCautela(
                [
                    (desc, item[0].replace("\n", " ")),
                    (
                        str(keys[1]).replace("\n", "").upper(),
                        item[1].replace("\n", " "),
                    ),
                    (
                        str(keys[2]).replace("\n", "").upper(),
                        item[2].replace("\n", " "),
                    ),
                    (
                        str(keys[3]).replace("\n", "").upper(),
                        item[3].replace("\n", " "),
                    ),
                ]
            )
        )

        print(item)

    for item in equips:
        await reinserir_estoque(db, item)

    if not query.nome_epis:
        query.nome_epis = ",".join([item["DESCRICAO"] for item in equips])

    registro_cancelada = RegistrosCautelasCanceladas(cautela_id=id_cautela)
    db.session.add(registro_cancelada)
    db.session.commit()


async def reinserir_estoque(db: SQLAlchemy, item: ItemCautela):
    estoque_grade = db.session.query(EstoqueGrade).all()
    estoque_geral = db.session.query(EstoqueEPI).all()

    def verify_nome_epi(item_filter: EstoqueGrade | EstoqueEPI) -> bool:
        nome_epi: str = item_filter.nome_epi
        return any(
            [
                nome_epi.lower() == item["DESCRICAO"].lower(),
                nome_epi.lower() in item["DESCRICAO"].lower(),
                nome_epi.lower().replace(" ", "")
                == item["DESCRICAO"].lower().replace(" ", ""),
            ]
        )

    if len(estoque_grade) > 0:
        estoque_grade = list(filter(verify_nome_epi, estoque_grade))
        if len(estoque_grade) > 0:
            estoque_grade = (
                db.session.query(EstoqueGrade)
                .filter(EstoqueGrade.id == estoque_grade[-1].id)
                .first()
            )

    if len(estoque_geral) > 0:
        estoque_geral = list(filter(verify_nome_epi, estoque_geral))
        if len(estoque_geral) > 0:
            estoque_geral = (
                db.session.query(EstoqueEPI)
                .filter(EstoqueEPI.id == estoque_geral[-1].id)
                .first()
            )

    estoque_geral.qtd_estoque += int(item["QTDE"])
    estoque_grade.qtd_estoque += int(item["QTDE"])

    db.session.commit()


async def add_cautela_assinada(
    form: FormEnvioCautelaAssinada,
    query: RegistrosEPI,
    db: SQLAlchemy,
) -> None:
    new_cautela_assinada = CautelaAssinada(
        data_assinatura=datetime.now(
            pytz.timezone("America/Manaus"),
        )
    )
    with db.session.no_autoflush:
        query_funcionario = (
            db.session.query(Funcionarios)
            .filter(Funcionarios.nome_funcionario == query.funcionario)
            .first()
        )

        arquivo_assinado: FileStorage = form.arquivo_assinado.data
        temp_path_doc = Path(app.config["DOCS_PATH"]).joinpath(uuid4().hex)
        temp_path_doc.mkdir(parents=True, exist_ok=True)

        file_path = temp_path_doc.joinpath(arquivo_assinado.filename)
        await arquivo_assinado.save(file_path)

        new_cautela_assinada.filename = arquivo_assinado.filename
        async with aiofiles.open(file_path, "rb") as f:
            new_cautela_assinada.blob_doc = await f.read()

        with suppress(Exception):
            shutil.rmtree(temp_path_doc)

        new_cautela_assinada.cautela_id = query.id
        new_cautela_assinada.funcionario_id = query_funcionario.id

        db.session.add(new_cautela_assinada)
        db.session.commit()
