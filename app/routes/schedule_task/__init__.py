from os import path
from pathlib import Path

from celery import shared_task
from flask import Blueprint, Response
from flask import current_app as app
from flask import make_response, redirect, render_template, url_for
from flask_login import login_required
from flask_mail import Mail, Message
from flask_wtf import FlaskForm

from ...forms.schedule_task import TaskNotificacaoForm

template_folder = path.join(Path(__file__).parent.resolve(), "templates")
schedule_bp = Blueprint(
    "schedules", __name__, url_prefix="/schedule", template_folder=template_folder
)


@schedule_bp.get("/dash")
@login_required
def dash() -> Response:

    form: FlaskForm | TaskNotificacaoForm = TaskNotificacaoForm()
    page = "schedules.html"
    return make_response(render_template("index.html", page=page, form=form))


@schedule_bp.post("/new_schedule")
@login_required
def new_schedule() -> Response:

    # form: FlaskForm | TaskNotificacaoForm = TaskNotificacaoForm()

    # if form.validate_on_submit():

    #     days = [int(day) for day in form.days_of_week.data]

    return make_response(redirect(url_for("schedules.dash")))


@shared_task(bind=True, ignore_result=False)
def send_email(self, todo: str) -> None:

    mail = Mail(app)

    with app.app_context():

        msg = message_formatter(todo)
        mail.send(msg)


def message_formatter(todo: str) -> Message:

    import os
    from dotenv_vault import load_dotenv

    load_dotenv()

    from app import db
    from app.models import Users

    users = db.session.query(Users).all()
    copy_content = ["nicholas@robotz.dev"]

    for user in users:
        copy_content.append(user.email)

    with app.app_context():
        values = os.environ
        sendermail = values["MAIL_DEFAULT_SENDER"]

        funcionarios = ["funcionario1", "funcionario2"]

        sender_ = f"Notificação GuardEPI <{sendermail}>"
        assunto = "Notificação de troca de EPI"
        mensagem = render_template("assets/body_email.html", Funcionarios=funcionarios)

        return Message(assunto, sender=sender_, recipients=copy_content, html=mensagem)
