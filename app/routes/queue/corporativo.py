from flask import Flask, url_for, abort, flash, redirect
import os
from app import app
from app import db
from flask_login import login_required
from datetime import datetime
import openpyxl
from werkzeug.utils import secure_filename
import re
from app.Forms import *
from app.models import *
from typing import Type
import pandas as pd

tipo = db.Model


def getModel(form) -> Type[tipo]:

    forms = {
        'funcionarios': Funcionarios,
        'empresas': Empresa,
        'departamentos': Departamento,
        'cargos': Cargos
    }

    return forms[form]


@app.route("/importacao_corporativo/<tipo>", methods=["POST"])
@login_required
def importacao_corporativo(tipo: str):

    try:
        form = IMPORTEPIForm()
        model = getModel(tipo.lower())
        if form.validate_on_submit():

            doc = form.arquivo.raw_data[0]

            docname = secure_filename(doc.filename)
            doc.save(os.path.join(app.config['CSV_TEMP_PATH'], f"{docname}"))
            doc_path = os.path.join(app.config['CSV_TEMP_PATH'], f"{docname}")

            df = pd.read_excel(doc_path)
            df.columns = df.columns.str.lower()
            
            if df.get('data_admissao', None):
                df['data_admissao'] = pd.to_datetime(
                    df['data_admissao'], errors='coerce')

            data = []
            for _, row in df.iterrows():
                data_info = row.to_dict()
                appends = model(**data_info)
                data.append(appends)

            db.session.add_all(data)
            db.session.commit()

        flash("Informação cadastrada com sucesso!", "success")
        return redirect(url_for(tipo))

    except Exception as e:
        abort(500)
