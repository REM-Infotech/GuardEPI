from pathlib import Path

from flask import Blueprint
from flask import current_app as app
from flask import send_from_directory

serve = Blueprint("serve", __name__)


@serve.get("/serve_img/<filename>")
def serve_img(filename: str):
    """
    Route to serve an image file.
    This route handles GET requests to serve an image file from a specified directory.
    The filename is provided as a URL parameter.
    Args:
        filename (str): The name of the image file to be served.
    Returns:
        Response: A Flask response object that sends the requested image file from the directory specified in the app configuration.
    """
    path_img = Path(app.config["IMAGE_TEMP_PATH"])
    return send_from_directory(path_img, filename)
