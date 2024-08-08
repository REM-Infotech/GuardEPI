from flask import (render_template, abort, session, request, redirect, url_for)
from flask_login import login_required

from app import app

from app.models import Groups
from app.Forms import CreateGroup
from app.decorators import read_perm, update_perm, create_perm, set_endpoint
import json
import uuid
import os

@app.before_request
def setgroups():
    
    if request.endpoint == "groups":
        if not session.get("uuid_groups", None):
            
            session["uuid_groups"] = str(uuid.uuid4())
            pathj = os.path.join(app.config['Temp_Path'], f"{session["uuid_groups"]}.json")
            
            if os.path.exists(pathj):
                os.remove(pathj)
            
            json_obj = json.dumps([])
            
            with open(pathj, 'w') as f:
                f.write(json_obj)

@app.route('/groups', methods=["GET"])
@login_required
@set_endpoint
@read_perm
def groups():

    try:

        form = CreateGroup()
        database = Groups.query.all()
        page = f'pages/config/{request.endpoint}.html'

        return render_template("index.html", form=form, database=database, page=page)

    except Exception as e:
        abort(500)


@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    
    list = [json.dumps(CreateGroup().users.data), json.dumps(CreateGroup().paginas.data), json.dumps(CreateGroup().permissions.data)]
    
    session["uuid_groups"]
    pathj = os.path.join(app.config['Temp_Path'], f"{session["uuid_groups"]}.json")
    
    with open(pathj, 'rb') as f:
        list_groups = json.load(f)

    list_groups.append(list)
    json_obj = json.dumps(list_groups)
        
    with open(pathj, 'w') as f:
        f.write(json_obj)

    item_html = render_template(
        'includes/add_groups.html', item=list_groups)
    return item_html


@app.route('/remove-groups', methods=['GET', 'POST'])
@login_required
def remove_groups():
    
    pathj = os.path.join(app.config['Temp_Path'], f"{session["uuid_groups"]}.json")
    json_obj = json.dumps([])
    
    with open(pathj, 'w') as f:
        f.write(json_obj)
        
    item_html = render_template('includes/add_groups.html')
    return item_html

@app.route("/create_group", methods = ["POST"])
@login_required
@create_perm
def create_group():
    
    form = CreateGroup()
    form_request = request.form
    
    mutable = {}
    
    for item in form_request:
        
        value = form_request[item]
        mutable.update({item: value})
    
    return redirect(url_for("groups", _scheme = 'https'))
