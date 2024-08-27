from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from app.misc import generate_pid
from configs import csp
from datetime import timedelta
import os


files_render = os.path.join(os.getcwd(), "app", "src")
app = Flask(__name__, template_folder = files_render, static_folder = files_render)
db = SQLAlchemy()
login_manager = LoginManager()
tlsm = Talisman()

app.config.from_object("app.default_config")
age = timedelta(days=7).max.seconds
db.init_app(app)
login_manager.init_app(app)
tlsm.init_app(app, content_security_policy=csp(),
              session_cookie_http_only=True,
              session_cookie_samesite='Lax',
              strict_transport_security=True,
              strict_transport_security_max_age=age,
              x_content_type_options= True,
              x_xss_protection=True)

login_manager.login_view = 'login'
login_manager.login_message = "Faça login para acessar essa página."
login_manager.login_message_category = "info"

# from app.models import init_database

# init_database()

from app import routes

