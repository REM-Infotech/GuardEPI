from celery import shared_task
from flask import current_app as app
from flask import render_template


@shared_task(bind=True, ignore_result=False)
def send_email(self, a: int, b: int) -> int:
    from dotenv import dotenv_values
    from flask_mail import Mail, Message

    from app import db
    from app.models import Users

    mail = Mail(app)

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

        msg = Message(assunto, sender=sender_, recipients=copy_content, html=mensagem)
        mail.send(msg)

    return a + b
