import secrets

from clear import clear
import os
from dotenv_vault import load_dotenv

load_dotenv()
from eventlet import listen
from eventlet.wsgi import server

from app import create_app

clear()
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

flask_app.app_context().push()

if __name__ == "__main__":

    def get_random_port() -> int:
        return secrets.randbelow(65535 - 1024) + 1024

    port = int(os.environ.get("PORT", get_random_port()))
    server(listen(("0.0.0.0", port)), flask_app, log=flask_app.logger)
