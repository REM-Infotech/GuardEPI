from app import app
from flask import render_template, redirect, url_for
from deep_translator import GoogleTranslator
from werkzeug.exceptions import HTTPException

tradutor = GoogleTranslator(source= "en", target= "pt")

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    
    name = tradutor.translate(error.name)
    desc = tradutor.translate(error.description)
    
    if error.code == 405:
        return redirect(url_for("dashboard"))

    return render_template("handler/index.html", name=name, 
                           desc=desc, code = error.code), error.code
