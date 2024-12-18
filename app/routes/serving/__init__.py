from pathlib import Path
from flask import Blueprint, send_from_directory
from flask import current_app as app

serve = Blueprint("serve", __name__)


@serve.get("/serve_img/<filename>")
def serve_img(filename: str):

    path_img = Path(app.config["IMAGE_TEMP_PATH"])
    return send_from_directory(path_img, filename)
