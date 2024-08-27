from flask import (jsonify, url_for, render_template, 
                   session, abort, flash, request, get_flashed_messages)
from flask_login import login_required

from app.Forms import Cautela
from app.models import (RegistrosEPI, ProdutoEPI, EstoqueEPI, RegistroSaidas,
                        Funcionarios, Empresa, EstoqueGrade)

from app.misc import generate_pid
from app.misc.generate_doc import (add_watermark, adjust_image_transparency,
create_EPI_control_sheet, create_watermark_pdf)

import os
import uuid
from datetime import datetime

from time import sleep
import json

from app import db
from app import app

from app.misc import format_currency_brl
from app.decorators import read_perm, set_endpoint, create_perm

@app.before_request
def setPerms():
    
    if request.endpoint == "Permissoes":
        if not session.get("uuid_Permissoes", None):
            
            session["uuid_Permissoes"] = str(uuid.uuid4())
            pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Permissoes"]}.json")
            
            if os.path.exists(pathj):
                os.remove(pathj)
            
            json_obj = json.dumps([])
            
            with open(pathj, 'w') as f:
                f.write(json_obj)
                
@app.route('/add_itens_perms', methods=['GET', 'POST'])
@login_required
def add_itens_perms():
    
    form = Cautela()
    list = [form.nome_epi.data, form.tipo_grade.data, form.qtd_entregar.data]

    pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Permissoes"]}.json")
    
    with open(pathj, 'rb') as f:
        list_epis = json.load(f)

    list_epis.append(list)
    json_obj = json.dumps(list_epis)
        
    with open(pathj, 'w') as f:
        f.write(json_obj)

    item_html = render_template(
        'includes/add_itens_perms.html', item=list_epis)

    # Retorna o HTML do item
    return item_html


@app.route('/remove_itens_perms', methods=['GET', 'POST'])
@login_required
def remove_itens_perms():
    
    pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Permissoes"]}.json")
    json_obj = json.dumps([])
    
    with open(pathj, 'w') as f:
        f.write(json_obj)
        
    item_html = render_template('includes/add_items.html')
    return item_html

@app.route("/Permissoes", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Permissoes():

    page = f"pages/config/{request.endpoint.lower()}.html"
    title = request.endpoint.capitalize()
    return render_template("index.html", page=page, title=title)

