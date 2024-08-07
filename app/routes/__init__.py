from app.routes.home import login
from app.routes.home import dashboard
from app.routes.home import queue
from app.routes import config

from app.routes.EPI import equipamentos
from app.routes.EPI import estoque
from app.routes.EPI import cautela
from app.routes.EPI import grades

from app.routes.Gestao import cargos
from app.routes.Gestao import departamentos
from app.routes.Gestao import empresas
from app.routes.Gestao import funcionarios

from app.routes.CRUD import create
from app.routes.CRUD import update
from app.routes.CRUD import delete

from app.routes import handler

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
        
        
    
#     pass