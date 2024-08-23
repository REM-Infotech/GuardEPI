from flask import (render_template, abort, session, send_from_directory)
from flask_login import login_required

from app import app
from app.models.users import Users
from app.Forms import IMPORTEPIForm, ProfileEditForm
from app.decorators import set_endpoint, read_perm

from app.misc import generate_pid

import os

@app.route('/users', methods=["GET"])
@login_required
@set_endpoint
@read_perm
def users():

    try:
        
        importForm = IMPORTEPIForm()
        database = Users.query.order_by(Users.login_time.desc()).all()

        page = 'pages/config/users.html'
        return render_template("index.html", page=page, database=database, importForm=importForm)

    except Exception as e:
        abort(500)