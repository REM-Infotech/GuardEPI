from celery import shared_task
from flask import render_template, current_app as app


@shared_task(bind=True, ignore_result=False)
def send_email(self, a: int, b: int) -> int:

    from app.models import Users
    from app import db
    from flask_mail import Message, Mail
    from dotenv import dotenv_values

    mail = Mail(app)

    users = db.session.query(Users).all()
    copy_content = []

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

    app.logger.info(str(a + b))

    print(a + b)

    return a + b
