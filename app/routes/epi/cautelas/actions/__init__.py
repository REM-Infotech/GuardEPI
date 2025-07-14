from datetime import datetime
from pathlib import Path
from uuid import uuid4

import aiofiles
import pytz
from flask_sqlalchemy import SQLAlchemy
from quart import current_app as app
from quart.datastructures import FileStorage

from app.forms.epi import FormEnvioCautelaAssinada
from app.models.EPI.cautelas import CautelaAssinada, EPIsCautela, RegistrosEPI
from app.models.Funcionários import Funcionarios


async def cancelamento_cautela(db: SQLAlchemy, id_cautela: int):
    query = db.session.query(EPIsCautela).all()

    return query


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
        async with aiofiles.open(file_path) as f:
            new_cautela_assinada.blob_doc = await f.read()

        new_cautela_assinada.cautela_id = query.id
        new_cautela_assinada.funcionario_id = query_funcionario.id

        db.session.add(new_cautela_assinada)
        db.session.commit()
