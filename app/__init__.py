import importlib
import os
from datetime import timedelta
from pathlib import Path

from celery import Celery, Task
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from app.logs.setup import initialize_logging
from configs import csp

app = None
db = None
login_manager = None
mail = None
celery_app = None


class AppFactory:

    def create_app(self):
        global app

        files_render = os.path.join(os.getcwd(), "app", "src")
        app = Flask(__name__, template_folder=files_render, static_folder=files_render)
        app.config.from_object("app.default_config")

        self.init_extensions(app)
        app.logger = initialize_logging()
        importlib.import_module("app.routes")

        global celery_app
        celery_app = self.celery_init_app(app)

        return app

    def init_extensions(self, app: Flask):

        global db, login_manager, mail
        mail = Mail()
        db = SQLAlchemy()
        login_manager = LoginManager()
        tlsm = Talisman()
        db.init_app(app)
        login_manager.init_app(app)
        tlsm.init_app(
            app,
            content_security_policy=csp(),
            session_cookie_http_only=True,
            session_cookie_samesite="Lax",
            strict_transport_security=True,
            strict_transport_security_max_age=timedelta(days=7).max.seconds,
            x_content_type_options=True,
            x_xss_protection=True,
        )

        login_manager.login_view = "login"
        login_manager.login_message = "Faça login para acessar essa página."
        login_manager.login_message_category = "info"

        with app.app_context():

            from app.models import init_database

            if not Path("is_init.txt").exists():
                with open("is_init.txt", "w") as f:
                    f.write(init_database())

    def celery_init_app(self, app: Flask) -> Celery:
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: object) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(app.name, task_cls=FlaskTask)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app


create_app = AppFactory().create_app
