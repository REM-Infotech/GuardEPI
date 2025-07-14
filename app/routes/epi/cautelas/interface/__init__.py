from datetime import datetime
from typing import TypedDict

from app.models.EPI.cautelas import CautelaAssinada


class ItemsEPIDict(TypedDict):
    NOME_EPI: str
    GRADE: str
    QTD: str


class RegistrosEPIClass:
    id: int = None
    nome_epis: str = None
    valor_total: str = None
    funcionario: str = None
    data_solicitacao: datetime = None
    filename: str = None
    blob_doc: bytes = None
    documentos_assinados: list = None

    def __init__(self, **kwargs) -> None:
        for item in dir(RegistrosEPIClass):
            if item.startswith("_"):
                continue

            to_add = kwargs.get(item)
            if to_add:
                if item == "documentos_assinados":
                    if len(to_add) > 0:
                        val: CautelaAssinada = to_add[-1]
                        setattr(self, item, val)
                        continue

                    elif len(to_add) == 0:
                        setattr(self, item, None)
                        continue

                setattr(self, item, to_add)
