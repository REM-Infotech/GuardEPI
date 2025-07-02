# from celery.schedules import crontab
import os
from datetime import timedelta
from pathlib import Path
from typing import Any

import quart_flask_patch  # noqa: F401
from celery import Celery
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, init, migrate, upgrade
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from quart import Quart

from app.logs.setup import initialize_logging

load_dotenv()

path_parent = Path(__file__).parent.resolve()

template_folder = path_parent.joinpath("templates")
static_folder = path_parent.joinpath("static")

app = Quart(__name__, template_folder=template_folder, static_folder=static_folder)

mail = Mail()
db = SQLAlchemy()
celery_app = None
migrate_ = Migrate()
login_manager = LoginManager()
celery_app = Celery(app.import_name)
objects_config = {
    "development": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig",
    "testing": "app.config.TestingConfig",
}


def celery_init(app: Quart) -> Celery:
    """
    Initialize a Celery instance with the given Quart application.
    This function sets up a Celery instance, configures it to use threads as the worker pool,
    imports configurations from the Quart app, and defines a custom task class that ensures
    tasks are executed within the Quart application context.
    Args:
        app (Quart): The Quart application instance.
    Returns:
        Celery: The configured Celery instance.
    """

    """ Instancia do Celery"""

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


def create_app() -> Quart:
    env_ambient = os.getenv("AMBIENT_CONFIG")
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
    migrate_.init_app(app)
    with app.app_context():
        if os.environ.get("MIGRATE") and os.environ.get("MIGRATE").lower() == "true":
            migrate_.init_app(app, db, directory="migrations")
            if not Path(__file__).cwd().joinpath("migrations").exists():
                init()

            migrate(directory="migrations", message="Initial migration")
            upgrade(directory="migrations")

    return app


def init_extensions(app: Quart) -> None:
    mail.init_app(app)
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
        from .models import init_database

        init_database(app, db)
