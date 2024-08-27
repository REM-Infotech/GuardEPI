from flask import (render_template, abort, flash, request, 
                   redirect, url_for, session)
from flask_login import login_required

from app import app
from app import db

from app.models import Groups, Users
from app.Forms import CreateGroup
from app.decorators import (read_perm, set_endpoint, 
                            create_perm, update_perm, delete_perm)

import json
import logging

@app.route('/groups', methods=["GET"])
@login_required
@set_endpoint
@read_perm
def groups():

    try:

        session["name_group"] = ""
        form = CreateGroup()
        database = Groups.query.all()
        page = f'pages/config/{request.endpoint}.html'

        return render_template("index.html", form=form, database=database, page=page)

    except Exception as e:
        logging.exception(str(e))
        abort(500)


@app.route("/create_group", methods=["POST"])
@login_required
@create_perm
def create_group():

    form = CreateGroup()
    group = Groups.query.filter(Groups.name_group == form.nome.data).first()

    if not group:

        perms_default = {
            "dashboard": {
                "permissoes": [
                    "READ"]
            }
        }

        grp = Groups(
            name_group=form.nome.data,
            members=json.dumps(form.membros.data),
            perms=json.dumps(perms_default)
        )
        
        for usr in form.membros.data:
            
            user = Users.query.filter(Users.login == usr).first()
            list_group = json.loads(user.grupos)
            
            for grupo in list_group:
                if grupo != form.nome.data:
                    
                    list_group.append(form.nome.data)
                    break
            
            user.grupos = json.dumps(list_group)
            
        db.session.add(grp)
        db.session.commit()
        flash("Grupo criado com sucesso!")
        
    else:
        flash("Grupo já existente!", "error")

    return redirect(url_for("groups", _scheme='https'))

@app.route("/setEditGroup/<item>", methods = ["GET"])
@login_required
@update_perm
def setEditGroup(item: int):
    
    database = Groups.query.filter(Groups.id == item).first()
    session["name_group"] = database.name_group
    form = CreateGroup(**{'nome': database.name_group,
                          'membros': json.loads(database.members)})
    
    route = request.referrer.replace("https://", "").replace("http://", "")
    route = route.split("/")[1]
    
    grade_results = f"pages/forms/{route}/edit.html"
    return render_template(grade_results, form=form, tipo=route, id=item)


@app.route("/update_group", methods = ["POST"])
@login_required
@update_perm
def update_group():
    
    form = CreateGroup()
    
    gp_name = form.nome.data
    
    if len(form.membros.data) == 0:
        flash("Grupo requer ao menos 1 usuário", "error")
        return redirect(url_for("groups", _scheme='https'))
    
    ## Query database grupo com o nome que está no Form
    database = Groups.query.filter(Groups.name_group == gp_name).first()
    
    ## Se o nome não foi encontrado, ele foi alterado
    if not database:
        
        ## Refaço a busca
        database = Groups.query.filter(
            Groups.name_group == session["name_group"]).first()
        
    ## Seto as alterações do database
    database.name_group = gp_name
    database.members = json.dumps(form.membros.data)
    
    ## Loop for nos membros do grupo
    for usr in form.membros.data:
        
        user = Users.query.filter(Users.login == usr).first()
        list_group = json.loads(user.grupos)
        
        ## Se o usuário não está na lista de membros
        if not usr in form.membros.data:
            
            ## Removo da lista de grupos na qual ele faz parte
            list_group.remove(session["name_group"])

        ## Caso o grupo não esteja na lista de grupos no qual o usuário faz parte
        elif not form.nome.data in list_group:
            list_group.append(form.nome.data)
        
        ## Caso nome do grupo tenha sido alterado
        if session["name_group"] != form.nome.data:
            
            list_group.remove(session["name_group"])
            list_group.append(form.nome.data)
            
        user.grupos = json.dumps(list_group)
        
    db.session.commit()
    
    flash("Alterações salvas com sucesso!")
    return redirect(url_for("groups", _scheme='https'))

@app.route("/deleteGroup/<id>", methods = ["POST"])
@login_required
@delete_perm
def deleteGroup(id: int):
    
    template = "includes/show.html"
    
    ## Query do grupo a ser deletado
    dbase_group = Groups.query.filter(Groups.id == id).first()
    nome_grupo: str = dbase_group.name_group
    
    ## Se o grupo a ser deletado for root, ele vai bloquear
    if nome_grupo == "Grupo Root":
        message = "Grupo Root não pode ser deletado!"
        return render_template(template, message = message)
    
    ## Loop for nos membros
    for user in json.loads(dbase_group.members):
        
        ## Query do user
        query_user = Users.query.filter(Users.login == user).first()
        
        ## Se o usuário nao existir, continua
        if not query_user:
            continue
        
        ## Ver os grupos no qual o usuário está
        list_grupos = json.loads(query_user.grupos)
        
        for grupo in list_grupos:
            
            ## Se o grupo a ser deletado estiver na lista
            if grupo == nome_grupo:
                
                ## Remove o grupo da lista de grupos que o usuário faz parte
                list_grupos.remove(grupo)
                break
            
        ## Atualiza a lista de grupos do usuário
        query_user.grupos = json.dumps(list_grupos)
        db.session.commit()
        
    db.session.delete(dbase_group)
    db.session.commit()
    
    
    message = "Grupo deletado com sucesso!"
    return render_template(template, message = message)