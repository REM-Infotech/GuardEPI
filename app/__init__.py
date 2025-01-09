from datetime import timedelta
from pathlib import Path
from typing import Any

from celery import Celery

# from celery.schedules import crontab
from dotenv import dotenv_values
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

from app.logs.setup import initialize_logging

app = None
db = None
login_manager = None
mail = None
celery_app = None

objects_config = {
    "development": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig",
    "testing": "app.config.TestingConfig",
}


def celery_init(app: Flask) -> Celery:
    """
    Initialize a Celery instance with the given Flask application.
    This function sets up a Celery instance, configures it to use threads as the worker pool,
    imports configurations from the Flask app, and defines a custom task class that ensures
    tasks are executed within the Flask application context.
    Args:
        app (Flask): The Flask application instance.
    Returns:
        Celery: The configured Celery instance.
    """

    """ Instancia do Celery"""
    celery_app = Celery(app.import_name)

    """ Worker Pool usa Threads """
    celery_app.conf.worker_pool = "threads"

    """ Importa configurações """
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.update(broker_connection_retry_on_startup=True)

    """ Define TaskBase """
    TaskBase = celery_app.Task

    """ Class ContextTask """

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs) -> Any:
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    """ Redefine property Task """
    celery_app.Task = ContextTask
    return celery_app


def create_app() -> Flask:
    global app

    template_folder = Path(__file__).parent.resolve().joinpath("templates").resolve()
    static_folder = Path(__file__).parent.resolve().joinpath("static").resolve()
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    env_ambient = dotenv_values(".env")["AMBIENT_CONFIG"]
    ambient = objects_config[env_ambient]

    app.config.from_object(ambient)

    init_extensions(app)
    app.logger = initialize_logging()
    from app.routes import register_routes

    register_routes(app)

    global celery_app
    celery_app = celery_init(app)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    app.extensions["mail"] = mail

    return app


def init_extensions(app: Flask) -> None:
    global db, login_manager, mail
    mail = Mail(app)
    db = SQLAlchemy()
    login_manager = LoginManager()

    db.init_app(app)
    login_manager.init_app(app)
    csp = app.config["CSP"]

    if not app.debug:
        tlsm = Talisman()
        tlsm.init_app(
            app,
            content_security_policy=csp,
            session_cookie_http_only=True,
            session_cookie_samesite="Lax",
            strict_transport_security=True,
            strict_transport_security_max_age=timedelta(days=7).max.seconds,
            x_content_type_options=True,
            x_xss_protection=True,
        )

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Faça login para acessar essa página."
    login_manager.login_message_category = "info"

    with app.app_context():
        from .models import init_database, Users

        if not Path("is_init.txt").exists():
            passw = init_database(app, db)
            with open("is_init.txt", "w") as f:
                f.write(passw)

        elif not db.engine.dialect.has_table(db.engine.connect(), Users.__tablename__):
            passw = init_database(app, db)
            with open("is_init.txt", "w") as f:
                f.write(passw)
