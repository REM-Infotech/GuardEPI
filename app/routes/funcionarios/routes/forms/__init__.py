# noqa: D104


from quart import Blueprint

forms = Blueprint(__name__.replace(".", "_"), __name__, url_prefix="/forms")
