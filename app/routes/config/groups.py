from flask import (render_template, abort, session, request, redirect, url_for)
from flask_login import login_required

from app import app

from app.models import Groups
from app.Forms import CreateGroup
from app.decorators import read_perm, update_perm, create_perm, set_endpoint
import json

@app.route('/groups', methods=["GET"])
@login_required
@set_endpoint
@read_perm
def groups():

    try:

        session["groups_lista"] = []
        form = CreateGroup()
        database = Groups.query.all()
        page = f'pages/config/{request.endpoint}.html'

        return render_template("index.html", form=form, database=database, page=page)

    except Exception as e:
        abort(500)


@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():

    form = CreateGroup()
    session["groups_lista"].append(
        [json.dumps(form.users.data), json.dumps(form.paginas.data), json.dumps(form.permissions.data)])

    item_html = render_template(
        'includes/add_items.html', item=session["groups_lista"])
    return item_html


@app.route('/remove-groups', methods=['GET', 'POST'])
@login_required
def remove_groups():

    session["groups_lista"] = []
    item_html = render_template('includes/add_items.html')
    return item_html

@app.route("/create_group", methods = ["GET"])
@login_required
@create_perm
def create_group():
    
    form = CreateGroup()
    form_request = request.form
    
    return redirect(url_for("groups", _scheme = 'https'))
