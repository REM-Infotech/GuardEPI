from clear import clear
from eventlet import listen
from eventlet.wsgi import server

from app import create_app

clear()
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

flask_app.app_context().push()

if __name__ == "__main__":
    server(listen(("localhost", "5000")), flask_app, log=flask_app.logger, debug=True)
