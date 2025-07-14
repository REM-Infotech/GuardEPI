import json
from datetime import datetime
from pathlib import Path
from typing import List
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from quart import current_app as app
from quart import session

from app.forms.epi import Cautela
from app.models.EPI.cautelas import EPIsCautela, RegistrosEPI
from app.models.EPI.equipamento import ProdutoEPI
from app.models.EPI.estoque import EstoqueEPI, EstoqueGrade, RegistroSaidas


async def subtract_estoque(form: Cautela, db: SQLAlchemy, nomefilename: str) -> list:
    try:
        epis_lista = []
        para_registro: list[RegistroSaidas] = []
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

            async def query_data() -> tuple[
                ProdutoEPI | None, EstoqueEPI | None, EstoqueGrade | None
            ]:
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

                return equip, data_estoque, estoque_grade

            async def verificar_saldo_estoque() -> bool:
                if estoque_grade:
                    if all(
                        [estoque_grade.qtd_estoque > 0, data_estoque.qtd_estoque > 0]
                    ):
                        return True

                return False

            equip, data_estoque, estoque_grade = await query_data()

            if await verificar_saldo_estoque():
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

        registrar.nome_epis = ",".join([str(item.nome_epi) for item in para_registro])

        secondary: List[EPIsCautela] = []
        for epi in para_registro:
            registro_secondary = EPIsCautela(cod_ref=str(uuid4()))
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
