import os
import importlib
from configs import csp
from pathlib import Path
from datetime import timedelta


from flask import Flask
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = None
db = None
login_manager = None


class AppFactory:

    def create_app(self):
        global app

        files_render = os.path.join(os.getcwd(), "app", "src")
        app = Flask(__name__, template_folder=files_render, static_folder=files_render)
        app.config.from_object("app.default_config")

        self.init_extensions(app)

        importlib.import_module("app.routes")
        return app

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
            strict_transport_security_max_age=timedelta(days=7).max.seconds,
            x_content_type_options=True,
            x_xss_protection=True,
        )

        login_manager.login_view = "login"
        login_manager.login_message = "Faça login para acessar essa página."
        login_manager.login_message_category = "info"

        with app.app_context():

            if not Path("is_init.txt").exists():
                with open("is_init.txt", "w") as f:
                    f.write("True")

                from app.models import init_database

                init_database()


create_app = AppFactory().create_app
