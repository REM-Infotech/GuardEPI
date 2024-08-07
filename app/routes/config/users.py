from flask import (render_template, abort)
from flask_login import login_required

from app import app
from app.models.users import Users
from app.Forms.globals import IMPORTEPIForm
from app.decorators import set_endpoint

@app.route('/users', methods=["GET"])
@login_required
@set_endpoint
def users():

    try:
        importForm = IMPORTEPIForm()
        database = Users.query.order_by(Users.login_time.desc()).all()

        page = 'pages/config/users.html'
        return render_template("index.html", page=page, database=database, importForm=importForm)

    except Exception as e:
        abort(500)
