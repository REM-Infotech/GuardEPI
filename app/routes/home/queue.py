# import os
# from typing import Type

# import pandas as pd
# from flask import make_response, send_file, current_app as app
# from flask_login import login_required
# from sqlalchemy import LargeBinary

# from app.models import (
#     Cargos,
#     Departamento,
#     Empresa,
#     EstoqueEPI,
#     EstoqueGrade,
#     Funcionarios,
#     GradeEPI,
#     ProdutoEPI,
# )

# tipo = db.Model


# def getModel(tipo: str) -> Type[tipo]:
#     model = {
#         "funcionarios": Funcionarios,
#         "empresas": Empresa,
#         "departamentos": Departamento,
#         "cargo.cargos": Cargos,
#         "estoque": EstoqueEPI,
#         "grade": GradeEPI,
#         "equipamentos": ProdutoEPI,
#         "estoque_grade": EstoqueGrade,
#     }

#     return model[tipo]
