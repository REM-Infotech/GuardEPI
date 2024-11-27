from flask import Flask

from app.routes import config, handler, terms_policy
from app.routes.CRUD import create, delete, update
from app.routes import cargos
from app.routes import dashboard
from app.routes.EPI import cautela, equipamentos, estoque, grades
from app.routes.Gestao import departamentos, empresas, funcionarios
from app.routes.home import login, queue, relatorio

__all__ = [
    login,
    queue,
    relatorio,
    equipamentos,
    estoque,
    cautela,
    grades,
    cargos,
    departamentos,
    empresas,
    funcionarios,
    create,
    update,
    delete,
    handler,
    config,
    terms_policy,
]


def register_blueprint(app: Flask):
    blueprints = [dashboard.dash, cargos.cargo_bp]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


# from app import app
# import json
# import os
# from flask import request

# @app.before_request
# def save_endpoints():

#     rar = request.url_rule.map._rules

#     endpoints = {}
#     for item in rar:

#         endpoints.update({item.endpoint: item.endpoint})

#     json_object = json.dumps(endpoints, indent=4)
#     with open("myJsn.json", "w") as outfile:
#         outfile.write(json_object)
