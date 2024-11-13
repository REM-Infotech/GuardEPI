from dotenv import load_dotenv
from pathlib import Path
from uuid import uuid4
import shutil
import os

from datetime import timedelta

load_dotenv()

login_db = os.getenv("login")
passwd_db = os.getenv("password")
host_db = os.getenv("host")
database_name = os.getenv("database")

# PARAMETROS PARA O APP FLASK
DEBUG = True
PDF_PATH = os.path.join(os.getcwd(), "PDF")
DOCS_PATH = os.path.join(os.getcwd(), "Docs")
TEMP_PATH = os.path.join(os.getcwd(), "Temp")
IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")
PDF_TEMP_PATH = os.path.join(TEMP_PATH, "pdf")


"""SqlAlchemy Config"""
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


"""FLASK CONFIG"""
PREFERRED_URL_SCHEME = "https"
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = True
PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds
SECRET_KEY = str(uuid4())

for paths in [DOCS_PATH, TEMP_PATH, IMAGE_TEMP_PATH, CSV_TEMP_PATH, PDF_TEMP_PATH]:

    shutil.rmtree(paths)
    Path(paths).mkdir(exist_ok=True)
