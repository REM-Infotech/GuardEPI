from flask import request, render_template, abort
from flask_login import login_required

from app import app
from app.decorators import set_endpoint, read_perm
from app.models import GradeEPI

from app.Forms import IMPORTEPIForm
from app.Forms import CadastroGrade

from app.misc import format_currency_brl


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
