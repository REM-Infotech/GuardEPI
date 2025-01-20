import json
import secrets
from importlib import import_module
from pathlib import Path

from flask import Blueprint, Response
from flask import current_app as app
from flask import make_response, redirect, request, session, url_for

template_folder = Path(__file__).parent.resolve().joinpath("templates")
config = Blueprint(
    "config", __name__, template_folder=template_folder, url_prefix="/config"
)


@config.before_request
def before_request_roles() -> None:
    """
    A function to be executed before handling requests to the roles configuration route.
    This function checks if the request path does not start with "/config/roles". If it does not,
    it ensures that a session variable "json_filename" is set. If the session variable is not set,
    it generates a new UUID, stores it in the session, and creates a temporary directory and JSON file
    associated with this UUID.
    The JSON file is initialized with an empty list.
    Side Effects:
        - Modifies the session to include a "json_filename" key with a generated UUID.
        - Creates a temporary directory and JSON file in the specified TEMP_PATH configuration.
        - Writes an empty JSON array to the created JSON file.
    """

    if request.endpoint == "config.cadastro_regra" and request.method == "GET":

        hex_name_json = secrets.token_hex(16)
        session["json_filename"] = hex_name_json

        path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()

        path_json.mkdir(exist_ok=True)

        json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

        with open(json_file, "w") as f:
            f.write(json.dumps([]))


@config.get("/")
def redirecting() -> Response:
    """
    Redirects to the 'Equipamentos' endpoint within the 'epi' blueprint.
    Returns:
        Response: A redirect response object to the 'epi.Equipamentos' URL.
    """

    return make_response(redirect(url_for("epi.Equipamentos")))


import_module(".users", __package__)
import_module(".groups", __package__)
import_module(".roles", __package__)
