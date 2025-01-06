import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from celery.schedules import crontab
from dotenv import dotenv_values
from pytz import timezone


class Configurator:

    env_file = ".env"

    def __init__(self):

        debug_flag = Path(".debug").exists()
        if debug_flag:
            self.env_file = ".testing"

    def get_configurator(self):

        class ConfigObject:

            values = dotenv_values()

            login_db = values.get("LOGIN")
            passwd_db = values.get("PASSWORD")
            host_db = values.get("HOST")
            database_name = values.get("DATABASE")
            redis_uri = values.get("REDIS_URI")

            # PARAMETROS PARA O APP FLASK
            DEBUG = True
            PDF_PATH = str(Path(__file__).cwd().joinpath("PDF"))
            DOCS_PATH = str(Path(__file__).cwd().joinpath("Docs"))
            TEMP_PATH = str(Path(__file__).cwd().joinpath("Temp"))
            IMAGE_TEMP_PATH = os.path.join(TEMP_PATH, "IMG")
            CSV_TEMP_PATH = os.path.join(TEMP_PATH, "csv")
            PDF_TEMP_PATH = os.path.join(TEMP_PATH, "pdf")

            MAIL_DEBUG = False
            MAIL_SUPPRESS_SEND = False
            MAIL_ASCII_ATTACHMENTS = False
            MAIL_SERVER = values["MAIL_SERVER"]
            MAIL_PORT = int(values["MAIL_PORT"])
            MAIL_USE_TLS = False
            MAIL_USE_SSL = False
            MAIL_USERNAME = values["MAIL_USERNAME"]
            MAIL_PASSWORD = values["MAIL_PASSWORD"]
            MAIL_DEFAULT_SENDER = values["MAIL_DEFAULT_SENDER"]

            """SqlAlchemy Config"""
            SQLALCHEMY_POOL_SIZE = 30  # Número de conexões na pool
            SQLALCHEMY_MAX_OVERFLOW = 10  # Número de conexões extras além da pool_size
            SQLALCHEMY_POOL_TIMEOUT = 30  # Tempo de espera para obter uma conexão
            SQLALCHEMY_POOL_RECYCLE = (
                1800  # Tempo (em segundos) para reciclar as conexões ociosas
            )
            SQLALCHEMY_POOL_PRE_PING = (
                True  # Verificar a saúde da conexão antes de usá-la
            )

            SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{login_db}:{passwd_db}@{host_db}:5432/{database_name}"

            SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
            SQLALCHEMY_TRACK_MODIFICATIONS = False

            """FLASK CONFIG"""
            PREFERRED_URL_SCHEME = "https"
            SESSION_COOKIE_HTTPONLY = False
            SESSION_COOKIE_SECURE = True
            PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds
            SECRET_KEY = str(uuid4())

            for paths in [
                DOCS_PATH,
                TEMP_PATH,
                IMAGE_TEMP_PATH,
                CSV_TEMP_PATH,
                PDF_TEMP_PATH,
            ]:
                if Path(paths).exists():
                    shutil.rmtree(paths)

                Path(paths).mkdir(exist_ok=True)

            now = datetime.now(timezone("America/Manaus"))
            hour = now.hour
            minute = now.minute

            CELERY = {
                "broker_url": f"{redis_uri}/0",
                "result_backend": f"{redis_uri}/1",
                "task_ignore_result": True,
                "beat_schedule": {
                    "notifications_epi": {
                        "task": "app.routes.schedule_task.send_email",
                        "schedule": crontab(hour=hour, minute=minute),
                    }
                },
                "timezone": "America/Sao_Paulo",
            }

        return ConfigObject


def csp() -> dict[str]:
    csp_vars = {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://code.jquery.com",
            "https://use.fontawesome.com",
            "",
            "'unsafe-inline'",
        ],
        "style-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "'unsafe-inline'",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://cdn-icons-png.flaticon.com",
            "https://domain.cliente.com",
        ],
        "connect-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
        ],
        "frame-src": [
            "'self'",
            "https://domain.cliente.com",
        ],
    }
    return csp_vars
