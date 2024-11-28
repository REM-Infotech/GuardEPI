from deep_translator import GoogleTranslator
from flask import redirect, render_template, url_for
from werkzeug.exceptions import HTTPException

from app import app


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    tradutor = GoogleTranslator(source="en", target="pt")
    name = tradutor.translate(error.name)
    desc = tradutor.translate(error.description)

    if error.code == 405:
        return redirect(url_for("dash.dashboard"))

    return (
        render_template("handler/index.html", name=name, desc=desc, code=error.code),
        error.code,
    )
