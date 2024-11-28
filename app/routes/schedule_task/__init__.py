from os import path
from pathlib import Path

from celery import shared_task
from celery.schedules import crontab
from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from pytz import timezone

from app import celery_app

from ...Forms import schedule_task

template_folder = path.join(Path(__file__).parent.resolve(), "templates")
schedule_bp = Blueprint(
    "schedules", __name__, url_prefix="/schedule", template_folder=template_folder
)


@schedule_bp.get("/dash")
def dash():

    form: FlaskForm = schedule_task.TaskNotificacaoForm()
    page = "schedules.html"
    return render_template("index.html", page=page, form=form)


@schedule_bp.post("/new_schedule")
def new_schedule():

    form: FlaskForm = schedule_task.TaskNotificacaoForm()

    if form.validate_on_submit():
        pass

        celery_app.add_periodic_task(
            crontab(hour=7, minute=30, day_of_week={1, 2, 3, 4, 5}),
            send_email.s(form.todo.data),
            name=form.nome_task.data,
            timezone=timezone(form.timezone),
        )

    return redirect(url_for("schedule_bp.dash"))


@shared_task(bind=True, ignore_result=False)
def send_email(self, todo: str):

    mail = Mail(app)

    with app.app_context():

        msg = message_formatter(todo)
        mail.send(msg)

    return


def message_formatter(todo: str) -> Message:

    from dotenv import dotenv_values

    from app import db
    from app.models import Users

    users = db.session.query(Users).all()
    copy_content = ["nicholas@robotz.dev"]

    for user in users:
        copy_content.append(user.email)

    with app.app_context():
        values = dotenv_values()
        sendermail = values["MAIL_DEFAULT_SENDER"]

        funcionarios = ["funcionario1", "funcionario2"]

        sender_ = f"Notificação GuardEPI <{sendermail}>"
        assunto = "Notificação de troca de EPI"
        mensagem = render_template("assets/body_email.html", Funcionarios=funcionarios)

        return Message(assunto, sender=sender_, recipients=copy_content, html=mensagem)
