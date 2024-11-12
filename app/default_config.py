from dotenv import load_dotenv, dotenv_values
from datetime import timedelta
from pathlib import Path
from uuid import uuid4
import os

load_dotenv()
values = dotenv_values()

login_db = values.get("login")
passwd_db = values.get("password")
host_db = values.get("host")
database_name = values.get("database")


# FLASK-MAIL CONFIG
DEBUG = True
MAIL_SERVER = values["MAIL_SERVER"]
MAIL_PORT = int(values["MAIL_PORT"])
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = values["MAIL_USERNAME"]
MAIL_PASSWORD = values["MAIL_PASSWORD"]
MAIL_DEFAULT_SENDER = values["MAIL_DEFAULT_SENDER"]

# SQLALCHEMY CONFIG
debug = values.get("DEBUG", "False").lower() in ("true", "1", "t", "y", "yes")

# SqlAlchemy config

SQLALCHEMY_POOL_SIZE = 30  # Número de conexões na pool
SQLALCHEMY_MAX_OVERFLOW = 10  # Número de conexões extras além da pool_size
SQLALCHEMY_POOL_TIMEOUT = 30  # Tempo de espera para obter uma conexão
SQLALCHEMY_POOL_RECYCLE = 1800  # Tempo (em segundos) para reciclar as conexões ociosas
SQLALCHEMY_POOL_PRE_PING = True  # Verificar a saúde da conexão antes de usá-la

SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{login_db}:{passwd_db}@{host_db}:5432/{database_name}"
)
SQLALCHEMY_BINDS = {"cachelogs": "sqlite:///cachelogs.db"}
SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
SQLALCHEMY_TRACK_MODIFICATIONS = False


# FLASK CONFIG
PREFERRED_URL_SCHEME = "https"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds
SECRET_KEY = str(uuid4())

DOCS_PATH = os.path.join(os.getcwd(), "Docs")
TEMP_PATH = os.path.join(os.getcwd(), "Temp")
IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")

for paths in [DOCS_PATH, TEMP_PATH, IMAGE_TEMP_PATH, CSV_TEMP_PATH]:
    Path(paths).mkdir(exist_ok=True)
