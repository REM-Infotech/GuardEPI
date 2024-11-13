from app import app
from flask import render_template, redirect, url_for
from deep_translator import GoogleTranslator
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def handle_http_exception(error):

    tradutor = GoogleTranslator(source="en", target="pt")
    name = tradutor.translate(error.name)
    desc = tradutor.translate(error.description)

    if error.code == 405:
        return redirect(url_for("dashboard"))

    return (
        render_template("handler/index.html", name=name, desc=desc, code=error.code),
        error.code,
    )
