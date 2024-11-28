from flask import abort, render_template, request
from flask_login import login_required

from app import app
from app.decorators import read_perm, set_endpoint
from app.Forms import CadastroGrade, IMPORTEPIForm
from app.misc import format_currency_brl
from app.models import GradeEPI


@app.route("/Grade")
@login_required
@set_endpoint
@read_perm
def Grade():
    try:
        title = "Grades"
        page = f"pages/epi/{request.endpoint.lower()}.html"
        DataTables = "js/DataTables/epi/grade.js"
        form = CadastroGrade()
        importForm = IMPORTEPIForm()
        database = GradeEPI.query.all()
        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            DataTables=DataTables,
            form=form,
            importForm=importForm,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))
