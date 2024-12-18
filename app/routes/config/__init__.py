# import json

# from deep_translator import GoogleTranslator
# from flask import abort, flash, redirect, render_template, request, session, url_for
# from flask_login import login_required

# from app import app, db
# from app.decorators import create_perm, delete_perm, update_perm
# from app.forms import (
#     AdmChangeEmail,
#     AdmChangePassWord,
#     ChangeEmail,
#     ChangePassWord,
#     CreateUserForm,
# )
# from app.models import Groups, Users
# from app.routes.config import groups, perms, profile, users

# tradutor = GoogleTranslator(source="en", target="pt")
# __all__ = (users, profile, groups, perms)


# @app.route("/caduser_end", methods=["GET", "POST"])
# @login_required
# @create_perm
# def caduser_end():
#     form = CreateUserForm()
#     if request.method == "GET" and request.headers.get("HX-Request") == "true":
#         html = "pages/forms/admin/CreateUserForm.html"
#         return render_template(html, form=form)

#     elif request.method == "POST" and form.validate_on_submit():
#         usuario = Users(
#             login=form.login.data,
#             nome_usuario=form.nome.data,
#             email=form.email.data,
#             grupos=json.dumps(["Default"]),
#         )

#         usuario.senhacrip = form.password.data

#         try:
#             dbase_group = Groups.query.filter(Groups.name_group == "Default").first()
#             if dbase_group:
#                 list_groups = dbase_group.members
#                 extend_group = [form.login.data]
#                 if not list_groups:
#                     dbase_group.members = json.dumps(extend_group)

#                 else:
#                     list_groups = json.loads(dbase_group.members)
#                     list_groups.extend(extend_group)
#                     dbase_group.members = json.dumps(list_groups)

#             db.session.add(usuario)
#             db.session.commit()

#             flash("Usuário criado com sucesso!", "success")
#             return redirect(url_for("users"))

#         except Exception as e:
#             abort(500, description=str(e))

#     else:
#         if form.errors:
#             pass

#         else:
#             return redirect(url_for("users"))


# @app.route("/changepw_end", methods=["GET", "POST"])
# @login_required
# @update_perm
# def changepw_end():
#     try:
#         form = AdmChangePassWord()

#         html = "pages/forms/admin/AdmChangePasswordForm.html"
#         endpoint = (
#             request.referrer.replace("http://", "")
#             .replace("https://", "")
#             .split("/")[-1]
#         )
#         if endpoint == "profile_config":
#             form = ChangePassWord()
#             html = "pages/forms/user/ChangePasswordForm.html"

#         if form.validate_on_submit():
#             if form.new_password.data != form.repeat_password.data:
#                 flash("Senhas não coincidem")
#                 return redirect(url_for("users"))

#             login_usr = form.data.get("user_to_change", session.get("login"))
#             password = Users.query.filter_by(login=login_usr).first()
#             password.senhacrip = form.new_password.data
#             db.session.commit()

#             flash("Senha alterada com sucesso!", "success")
#             return redirect(url_for("users"))

#         return render_template(html, form=form)

#     except Exception as e:
#         abort(500, description=str(e))


# @app.route("/changemail_end", methods=["GET", "POST"])
# @login_required
# @update_perm
# def changemail_end():
#     try:
#         form = AdmChangeEmail()

#         html = "pages/forms/admin/AdmChangeMailForm.html"
#         endpoint = (
#             request.referrer.replace("http://", "")
#             .replace("https://", "")
#             .split("/")[-1]
#         )
#         if endpoint == "profile_config":
#             form = ChangeEmail()
#             html = "pages/forms/user/ChangeMailForm.html"

#         if form.validate_on_submit():
#             login_usr = form.data.get("user_to_change", session.get("login"))
#             mail = Users.query.filter_by(login=login_usr).first()
#             if form.new_email.data != form.repeat_email.data:
#                 flash("E-mails não coincidem")
#                 return redirect(url_for("users"))

#             mail.email = form.new_email.data
#             db.session.commit()

#             flash("E-mail alterado com sucesso!", "success")
#             return redirect(url_for("users"))

#         return render_template(html, form=form)

#     except Exception as e:
#         abort(500, description=str(e))


# @app.route("/delete_user/<usuario>", methods=["GET"])
# @login_required
# @delete_perm
# def delete_user(usuario: str):
#     try:
#         set_delete = False
#         atual_admin = session.get("login")
#         license_key = session.get("license_token", "")

#         message = ""
#         if session.get("tipo-usuario") == "super_admin":
#             query = Users.query.all()

#         elif session.get("tipo-usuario") == "admin":
#             query = Users.query.filter(Users.license_key == license_key).all()

#         for user in query:
#             if user.login == usuario:
#                 if usuario == atual_admin:
#                     message = "Você nao pode deletar seu usuário"
#                     break

#                 set_delete = True
#                 userto_delete = user
#                 message = "Usuário deletado com sucesso!"
#                 break

#         if set_delete is True:
#             db.session.delete(userto_delete)
#             db.session.commit()

#         template = "includes/show.html"
#         return render_template(template, message=message)

#     except Exception as e:
#         abort(500, description=str(e))
