from flask import *
from flask_login import *
from app.Forms import *
from app import app
from app.models import *


@app.route("/", methods = ["GET"])
def index():
    
    if session.get('_user_id', None) is not None:
        return redirect(url_for("dashboard"))
    
    return redirect(url_for("login"))

@app.route("/login", methods = ["GET", "POST"])
def login():
    
    if session.get('_user_id', None) is not None:
        return redirect(url_for("dashboard"))
    
    if not session.get('next'):
        session["next"] = request.args.get("next", url_for("dashboard"))
        
    location = session["next"]    
    form = LoginForm()
    if form.validate_on_submit():
        
        user = Users.query.filter_by(login = form.login.data).first()
        if user:
            check_pw = user.converte_senha(form.password.data)
            if check_pw:
                session["nome_usuario"] = user.nome_usuario
                session.pop("next")
                login_user(user, remember=form.keep_login.data)
                flash("Login Efetuado com sucesso!", "success")
                return redirect(location)
    
    return render_template("login.html", form = form)

@app.route("/logout", methods = ["GET"])
def logout():
    
    logout_user()
    flash("Sessão encerrada", "info")
    location = url_for("login")
    return redirect(location)