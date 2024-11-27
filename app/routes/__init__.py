from app.routes import config, handler, terms_policy
from app.routes.CRUD import create, delete, update
from app.routes.EPI import cautela, equipamentos, estoque, grades
from app.routes.Gestao import cargos, departamentos, empresas, funcionarios
from app.routes.home import dashboard, login, queue, relatorio

__all__ = [
    login,
    queue,
    dashboard,
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


from celery.result import AsyncResult
from flask import jsonify

from app import app

with app.app_context():
    from ..tasks import send_email


@app.route("/test_celery", methods=["GET"])
def test_celery():

    result = send_email.delay(15, 15)

    return jsonify({"result_id": result.id}), 200


@app.get("/result/<id>")
def task_result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }
