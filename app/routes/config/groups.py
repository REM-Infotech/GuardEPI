from flask import (render_template, abort, session)
from flask_login import login_required

from app import app

from app.models import Groups
from app.Forms import CreateGroup

@app.route('/groups', methods=["GET"])
@login_required
def groups():
    
    try:
        return render_template("index.html")
    
    except Exception as e:
        abort(500)
        
@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():

    form = CreateGroup()

    session["groups_lista"].append(
        [form.nome_epi.data, form.tipo_grade.data, form.qtd_entregar.data])

    item_html = render_template('includes/add_items.html', item=session["groups_lista"])
    return item_html


@app.route('/remove-groups', methods=['GET', 'POST'])
@login_required
def remove_groups():

    session["groups_lista"] = []
    item_html = render_template('includes/add_items.html')
    return item_html

