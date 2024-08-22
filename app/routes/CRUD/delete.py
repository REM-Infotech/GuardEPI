from flask_login import login_required
from flask import render_template

from app.decorators import delete_perm
from app.misc import *
from app.models import (ProdutoEPI, RegistrosEPI, EstoqueEPI, EstoqueGrade, RegistroEntradas,
                        GradeEPI, Empresa, Funcionarios, Departamento, Cargos, Groups,
                        ClassesEPI, ModelosEPI, Marcas, Fornecedores, Users)
from app import db
from typing import Type
from app import app
from app.routes.CRUD.miscs import get_models

tipo = db.Model


@app.route("/deletar_item/<database>/<id>", methods = ["POST"])
@delete_perm
def deletar_item(database: str, id: int):
    
    database = database.lower()
    model = get_models(database)
    dbase = model.query.filter(model.id == id).first()
    
    db.session.delete(dbase)
    db.session.commit()
    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message = message)
    