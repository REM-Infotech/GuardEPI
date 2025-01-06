from clear import clear  # pragma: no cover
from eventlet import listen  # pragma: no cover
from eventlet.wsgi import server  # pragma: no cover

from app import create_app  # pragma: no cover

clear()  # pragma: no cover
flask_app = create_app()  # pragma: no cover
celery_app = flask_app.extensions["celery"]  # pragma: no cover

flask_app.app_context().push()  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    server(
        listen(("localhost", 5002)), flask_app, log=flask_app.logger
    )  # pragma: no cover
