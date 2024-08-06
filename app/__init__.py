from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from app.misc import *
from configs import csp
from dotenv import dotenv_values
from datetime import timedelta
import os

docs_path = os.path.join(os.getcwd(), "Docs")
temp_path = os.path.join(os.getcwd(), "Temp")
image_temp = os.path.join(temp_path, "IMG")
csv_path = os.path.join(temp_path, "csv")
for paths in [docs_path, temp_path, image_temp, csv_path]:
    os.makedirs(paths, exist_ok=True)

files_render = os.path.join(os.getcwd(), "src")
app = Flask(__name__, template_folder = files_render, static_folder = files_render)
db = SQLAlchemy()
login_manager = LoginManager()
tlsm = Talisman()

login_db = dotenv_values()['DBLogin']
passwd_db = dotenv_values()['DBPassword']
host_db = dotenv_values()['DBHost']
database_name = dotenv_values()['Database']

database_uri = f"mysql://{login_db}:{passwd_db}@{host_db}/{database_name}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
app.config['PREFERRED_URL_SCHEME'] = "https"
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['Docs_Path'] = docs_path
app.config['Temp_Path'] = temp_path
app.config['IMAGE_TEMP_PATH'] = image_temp
app.config['CSV_TEMP_PATH'] = csv_path
app.secret_key = generate_pid()
app.make_response
age = timedelta(days=1).max.seconds
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

from app.Forms import *
from app.routes import *
from app.models import *