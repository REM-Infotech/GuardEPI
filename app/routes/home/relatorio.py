import os
from datetime import datetime
from typing import Type

import pandas as pd
from flask import abort, make_response, send_file
from flask_login import login_required
from sqlalchemy import LargeBinary

from app import app, db
from app.models import (
    Cargos,
    Departamento,
    Empresa,
    EstoqueEPI,
    EstoqueGrade,
    Funcionarios,
    GradeEPI,
    Groups,
    ProdutoEPI,
    RegistroEntradas,
    RegistrosEPI,
    Users,
)

tipo = db.Model


def get_models(tipo: str) -> Type[tipo]:

    models = {
        "equipamentos": ProdutoEPI,
        "grades": GradeEPI,
        "estoque": EstoqueEPI,
        "estoque_grade": EstoqueGrade,
        "entradas": RegistroEntradas,
        "cautelas": RegistrosEPI,
        "funcionarios": Funcionarios,
        "empresas": Empresa,
        "departamentos": Departamento,
        "cargo_bp.cargos": Cargos,
        "users": Users,
        "groups": Groups,
    }

    return models[tipo]


@app.route("/gerar_relatorio/<dbase>")
@login_required
def gerar_relatorio(dbase: str):

    try:
        now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")  # Change colon to hyphen
        filename = f"Relatório {dbase.capitalize()} - {now}.xlsx"
        file_path = os.path.join(app.config["CSV_TEMP_PATH"], filename)

        model = get_models(dbase.lower())
        query = model.query.all()

        data = []
        for item in query:

            it: dict = item.__dict__
            for column in item.__table__.columns:
                if isinstance(column.type, LargeBinary):
                    it.pop(column.name)

            it.pop("_sa_instance_state")
            data.append(it)

        df = pd.DataFrame(data)

        df.to_excel(file_path, index=False)

        response = make_response(send_file(f"{file_path}", as_attachment=True))
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        abort(500, description=str(e))
