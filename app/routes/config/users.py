from flask import abort, render_template
from flask_login import login_required

from app import app
from app.models.users import Users


@app.route("/users", methods=["GET"])
@login_required
def users():
    try:

        database = Users.query.order_by(Users.login_time.desc()).all()

        page = "pages/config/users.html"
        return render_template(
            "index.html",
            page=page,
            database=database,
        )

    except Exception as e:
        abort(500, description=str(e))
