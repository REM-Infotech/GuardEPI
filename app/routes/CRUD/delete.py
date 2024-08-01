from flask_login import *
from flask import *

from app.misc import *
from app.models import *
from app import db
from typing import Type
from app import app

tipo = db.Model

def get_models(tipo: str) -> Type[tipo]:
    
    models = {"equipamentos": ProdutoEPI,
            "estoque": GradeEPI,
            "empresas": Empresa,
            "funcionarios": Funcionarios,
            "departamentos": Departamento,
            "cargos": Cargos}
    
    return models[tipo]

@app.route("/deletar_item/<database>/<id>", methods = ["POST"])
def deletar_item(database: str, id: int):
    
    database = database.lower()
    
    model = get_models(database)
    dbase = model.query.filter(model.id == id).first()
    
    db.session.delete(dbase)
    db.session.commit()
    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message = message)
    