import os
import importlib
from pathlib import Path
from flask import Flask
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from configs import csp
from datetime import timedelta


app = None
db = None
login_manager = None


class AppFactory:

    def init_extensions(self, app: Flask):

        global db, login_manager
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
            strict_transport_security_max_age=timedelta(days=1).max.seconds,
            x_content_type_options=True,
            x_xss_protection=True,
        )

        login_manager.login_view = "login"
        login_manager.login_message = "Faça login para acessar essa página."
        login_manager.login_message_category = "info"

        if not Path("dbinit.txt").exists():
            with app.app_context():
                from app.models import init_database

                init_database(app)

                with open("dbinit.txt", "w") as f:
                    f.write("TRUE")

    def create_app(self):

        global app
        files_render = os.path.join(os.getcwd(), "app", "src")
        app = Flask(__name__, template_folder=files_render, static_folder=files_render)
        app.config.from_object("app.default_config")
        self.init_extensions(app)
        importlib.import_module("app.routes", __name__)

        return app


create_app = AppFactory().create_app
