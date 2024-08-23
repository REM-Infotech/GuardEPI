from flask import session, flash, request, redirect, url_for, render_template
from flask_login import login_user, logout_user
from app.Forms import LoginForm
from app import app
from app.models.users import Users

import json


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
    
    location = str(session.get("next")) 
    form = LoginForm()
    if form.validate_on_submit():
        
        user = Users.query.filter_by(login = form.login.data).first()
        
        if user and user.converte_senha(form.password.data):
            
            session["username"] = form.login.data
            session["groups_usr"] = json.loads(user.grupos)
            session["nome_usuario"] = user.nome_usuario
            session.pop("next")
            login_user(user, remember=form.keep_login.data)
            flash("Login Efetuado com sucesso!", "success")
            
            if "?" in location:
                location = location.split("?")[0]
            
            return redirect(location)

        flash("Usuário/Senha Incorretos!", "error")
        
    return render_template("login.html", form = form)

@app.route("/logout", methods = ["GET"])
def logout():
    
    logout_user()
    flash("Sessão encerrada", "info")
    location = url_for("login")
    return redirect(location)