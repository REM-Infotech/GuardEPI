from flask import (
    abort,
    render_template,
    current_app as app,
    flash,
    redirect,
    url_for,
    request,
)
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.misc import format_currency_brl
from app.models import GradeEPI
from app.forms import CadastroGrade

from . import epi


@epi.route("/Grade")
@login_required
def Grade():
    try:
        title = "Grades"
        page = "grade.html"

        database = GradeEPI.query.all()
        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))


@epi.route("/Grade/cadastrar", methods=["GET", "POST"])
@login_required
def cadastrar_grade():

    endpoint = "Grade"
    act = "Cadastro"
    form = CadastroGrade()

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    if form.validate_on_submit():

        to_add = {}
        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit":
                to_add.update({key: value})

        grade = GradeEPI(**to_add)
        db.session.add(grade)
        db.session.commit()
        flash("Grade cadastrada com sucesso!", "success")
        return redirect(url_for("epi.grades"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/Grade/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_Grade(id):

    endpoint = "grade"
    act = "Cadastro"

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form = CadastroGrade()

    grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

    if request.method == "GET":
        form = CadastroGrade(**grade.__dict__)

    if form.validate_on_submit():

        form_data = form.data
        list_form_data = list(form_data.items())

        for key, value in list_form_data:
            if key != "csrf_token" or key != "submit" and value:
                setattr(grade, key, value)

        db.session.commit()

        flash("Grade editada com sucesso!", "success")
        return redirect(url_for("epi.grades"))

    return render_template(
        "index.html", page="form_base.html", form=form, endpoint=endpoint, act=act
    )


@epi.route("/grades/deletar/<int:id>", methods=["POST"])
@login_required
def deletar_Grade(id: int):

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    grade = db.session.query(GradeEPI).filter(GradeEPI.id == id).first()

    db.session.delete(grade)
    db.session.commit()

    template = "includes/show.html"
    message = "Informação deletada com sucesso!"
    return render_template(template, message=message)
