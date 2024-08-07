from app import app
from flask import render_template
from deep_translator import GoogleTranslator
from werkzeug.exceptions import HTTPException

tradutor = GoogleTranslator(source= "en", target= "pt")

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    
    name = tradutor.translate(error.name)
    desc = tradutor.translate(error.description)

    return render_template("handler/index.html", name=name, 
                           desc=desc, code = error.code), error.code
