import os
import pathlib
import json

from flask import (render_template, url_for, session, redirect, flash,
                   abort, send_from_directory, request)
from flask_login import login_required
from app import app, db

from werkzeug.utils import secure_filename

from app.models import Users, Groups
from app.Forms import ProfileEditForm

from app.decorators import read_perm
from app.misc import generate_pid


@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():

    try:
        username = str(session["username"])
        dbase = Users.query.filter_by(login=username).first()
        url_image = url_for('profile_pic')
        page = f'pages/{request.endpoint.lower()}.html'
        
        form = ProfileEditForm(**{
            "login": dbase.login,
            "nome_usuario": dbase.nome_usuario,
            "email": dbase.email
        }
        )
        
        if form.validate_on_submit():
          
            full_name = str(session["nome_usuario"])  
            if username == "root":
                return redirect
            
            user = Users.query.filter_by(login = username).first()
            
            if username != form.login.data:
                
                if not username == "root":
                    user.login = form.login.data
                    session["username"] = form.login.data
                    
                    group = Groups.query.all()
                    
                    for grupo in group:
                        
                        list_members: list = json.loads(grupo.members)
                        for membro in list_members:
                            
                            if username == membro:
                                list_members.remove(membro)
                                list_members.append(form.login.data)
                                break
                            
                        grupo.members = json.dumps(list_members)
                        db.session.commit()
                
            if full_name != form.nome_usuario.data:
                
                if not username == "root":
                    user.nome_usuario = form.nome_usuario.data
                    session["nome_usuario"] = form.nome_usuario.data
            
            if user.email != form.email.data:
                if not username == "root":
                    user.email = form.email.data
                
            if form.new_password.data:
                
                if user.converte_senha(form.old_password.data):
                    user.senhacrip = form.new_password.data
                    
                else:
                    flash("Senha Incorreta!", "error")
                    return redirect(url_for('profile')) 
                    
            if form.filename.data:
            
                file_pic = form.filename.data
                
                filename = secure_filename(file_pic.filename)
                filename = f"{generate_pid()}{filename}.png"
                original_path = os.path.join(
                    app.config['IMAGE_TEMP_PATH'], filename)
                
                file_pic.save(original_path)

                with open(original_path, 'wb') as file:
                    image_data = file.read()
                    
                user.filename = filename
                user.blob_doc = image_data 
                
            db.session.commit()
            
            flash("Alterações salvas com sucesso!", "success")
            return redirect(url_for('profile'))
            
        elif form.errors:
            flash("Erro interno", "error")
            return redirect(url_for('profile'))
        return render_template("index.html", page=page, form=form, url_image=url_image)

    except Exception as e:
        abort(500)


@app.route('/profile_pic', methods=["GET"])
@login_required
def profile_pic():

    try:

        user = session["username"]
        dbase = Users.query.filter_by(login=user).first()

        if not dbase.blob_doc:
            filename = "profile.png"
            original_path = app.config["SRC_IMG_PATH"]
            
        else:
            image_data = dbase.blob_doc
            filename = f"{generate_pid()}.png"
            original_path = os.path.join(
                app.config['IMAGE_TEMP_PATH'])

            with open(os.path.join(original_path, filename), 'wb') as file:
                file.write(image_data)
        
        parent_path = str(os.path.join(original_path))
        url = send_from_directory(parent_path, filename)

        return url

    except Exception as e:
        print(e)
        abort(500)
