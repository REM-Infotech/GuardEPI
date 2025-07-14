import json
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncGenerator, List
from uuid import uuid4

import aiofiles
from flask_sqlalchemy import SQLAlchemy
from quart import current_app as app
from quart import session

from app.forms.epi import Cautela
from app.models.EPI.cautelas import EPIsCautela, RegistrosEPI
from app.models.EPI.equipamento import ProdutoEPI
from app.models.EPI.estoque import EstoqueEPI, EstoqueGrade, RegistroSaidas
from app.routes.epi.cautelas.interface import ItemsEPIDict


class RegistrarSaida:
    async def dict_equipamentos_emissao(
        self,
    ) -> AsyncGenerator[ItemsEPIDict, Any, None]:
        path_json = Path(app.config["TEMP_PATH"]).joinpath(
            f"{session['uuid_Cautelas']}.json"
        )

        async with aiofiles.open(path_json, "r") as f:
            data_json = json.loads(await f.read())

        if len(data_json) == 0:
            raise ValueError("Adicione ao menos 1a EPI!")

        for item in data_json:
            yield ItemsEPIDict(**item)

    def __init__(self, form: Cautela, db: SQLAlchemy, nomefilename: str) -> None:
        self.form = form
        self.db = db
        self.nomefilename = nomefilename

    async def __call__(self) -> List[List[str]]:
        try:
            epis_lista = []
            para_registro: list[RegistroSaidas] = []
            list_epis_solict: list[list[str]] = []

            async for item_epi in self.dict_equipamentos_emissao():
                if not item_epi.get("NOME_EPI"):
                    continue

                nome_epi = item_epi["NOME_EPI"]
                grade_epi = item_epi.get("GRADE")
                qtd_entrega = item_epi.get("QTD")

                await self.query_data(
                    nome_epi,
                    grade_epi,
                )

                if await self.verificar_saldo_estoque():
                    list_epis_solict.append(
                        [str(nome_epi), qtd_entrega, grade_epi, self.equip.ca]
                    )
                    epis_lista.append(self.equip)
                    para_registro.append(
                        RegistroSaidas(
                            nome_epi=nome_epi,
                            grade_epi=grade_epi,
                            qtd_saida=int(qtd_entrega),
                            valor_total=self.equip.valor_unitario * int(qtd_entrega),
                        )
                    )

                    self.estoque_grade.qtd_estoque -= 1
                    self.data_estoque.qtd_estoque -= 1
                    valor_calc = self.equip.valor_unitario * int(qtd_entrega)

            await self.registro_saida(
                self.form.funcionario.data,
                valor_calc,
                para_registro,
            )

            return list_epis_solict

        except Exception as e:
            raise e

    async def query_data(
        self,
        nome_epi: str,
        grade_epi: str,
    ) -> tuple[ProdutoEPI | None, EstoqueEPI | None, EstoqueGrade | None]:
        session = self.db.session
        self.equip = session.query(ProdutoEPI).filter_by(nome_epi=nome_epi).first()

        self.data_estoque = (
            session.query(EstoqueEPI).filter_by(nome_epi=nome_epi).first()
        )
        self.estoque_grade = (
            session.query(EstoqueGrade)
            .filter_by(nome_epi=nome_epi, grade=grade_epi)
            .first()
        )

    async def verificar_saldo_estoque(
        self,
        estoque_grade: EstoqueGrade,
        data_estoque: EstoqueEPI,
    ) -> bool:
        if estoque_grade:
            return all([estoque_grade.qtd_estoque > 0, data_estoque.qtd_estoque > 0])

        return False

    async def registro_saida(
        self,
        nome_funcionario: str,
        valor_calculado: float | int,
        lista_para_registro: list[RegistrosEPI],
    ) -> None:
        registrar = RegistrosEPI(
            funcionario=nome_funcionario,
            data_solicitacao=datetime.now(),
            valor_total=valor_calculado,
        )

        registrar.nome_epis = ",".join(
            [str(item.nome_epi) for item in lista_para_registro]
        )

        secondary: List[EPIsCautela] = [
            EPIsCautela(
                cod_ref=str(uuid4()),
                epis_saidas_id=item.id,
                nomes_epis=registrar,
            )
            for item in lista_para_registro
        ]

        self.db.session.add(registrar)
        self.db.session.add_all(secondary)
        self.db.session.add_all(lista_para_registro)
        self.db.session.commit()
