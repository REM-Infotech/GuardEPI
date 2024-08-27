from flask_login import login_required
from flask import redirect, abort, flash, request
from flask_wtf import Form, FlaskForm

from werkzeug.utils import secure_filename
from flask_wtf.file import FileField
from sqlalchemy import LargeBinary

import os
from typing import Type

from app import app
from app import db

from app.misc import generate_pid
from app.decorators import create_perm
from app.models import ProdutoEPI
from app.routes.CRUD.miscs import get_models, getformCad


tipo = db.Model


@app.route("/cadastrar/<tipo>", methods=["POST"])
@login_required
@create_perm
def cadastrar(tipo: str):

    without_lower = tipo
    tipo = tipo.lower()

    try:
        form = getformCad(tipo)
        model = get_models(tipo.replace("edit_", ""))
        if form.validate_on_submit():
            kwargs = {}

            if tipo.lower() == "equipamentos":
                itens = model.query.filter_by(
                    nome_epi=form.nome_epi.data).first()

            elif tipo.lower() == "estoque":
                itens = model.query.filter(model.tipo_grade.contains(
                    str(form.tipo_grade.data).lower())).first()
                if itens is None:
                    kwargs.update({"ca": ProdutoEPI.query.filter_by(
                        nome_epi=form.nome_epi.data).first().ca})

            else:
                for md in model.__table__.columns:
                    form_fld = getattr(form, md.name, None)
                    if form_fld:
                        cln = md.name
                        itens = model.query.filter_by(
                            **{f"{cln}": form_fld.data}).first()
                        break

            path_img = ""
            if isinstance(model, list):
                model = model[0]

            if itens is None:
                for column in model.__table__.columns:
                    form_field = getattr(form, f"{column.name}", None)
                    if form_field:
                        data_insert = form_field.data
                        if isinstance(form_field, FileField):

                            file = form_field.data
                            
                            if file:
                                docname = secure_filename(file.filename)
                                now = generate_pid()
                                filename = f"{now}{docname}"
                                path_img = os.path.join(
                                    app.config['TEMP_PATH'], filename)
                                file.save(path_img)
                                kwargs[column.name] = filename

                        if "R$" in str(data_insert):
                            data_insert = float(str(data_insert).replace(
                                "R$ ", "").replace(".", "").replace(",", "."))

                        if data_insert:
                            kwargs.setdefault(column.name, data_insert)
                            
                    if isinstance(column.type, LargeBinary):
                        
                        if path_img:
                            with open(path_img, 'rb') as fileimg:
                                kwargs.setdefault(column.name, fileimg.read())

                new_itens = model(**kwargs)
                db.session.add(new_itens)
                db.session.commit()
                flash("Informação cadastrada com sucesso!", "success")

            else:
                flash("Item já cadastrado", "error")

            return redirect(f"{request.referrer}")

        if form.errors:
            for erros in list(form.errors):
                message = form.errors[erros][0]
                flash(message, "success")

    except Exception as e:
        abort(500)

    return redirect(f"/{without_lower}")
