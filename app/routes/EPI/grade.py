
from flask import abort, render_template
from flask_login import login_required

from app.forms import CadastroGrade
from app.misc import format_currency_brl
from app.models import GradeEPI

from . import epi


@epi.route("/Grade")
@login_required
def Grade():
    try:
        title = "Grades"
        page = "grades.html"

        form = CadastroGrade()

        database = GradeEPI.query.all()
        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            form=form,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))
