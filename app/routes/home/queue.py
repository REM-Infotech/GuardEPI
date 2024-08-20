from flask import url_for, abort, flash, redirect, send_file, make_response
from flask_login import login_required
import os
from app import app
from app import db

from sqlalchemy import LargeBinary
from werkzeug.utils import secure_filename
from typing import Type
import pandas as pd

from app.Forms.globals import IMPORTEPIForm
from app.models import Funcionarios, Empresa, Cargos, Departamento
from app.models import EstoqueEPI, GradeEPI, ProdutoEPI, EstoqueGrade

tipo = db.Model


def getModel(tipo: str) -> Type[tipo]:

    model = {
        'funcionarios': Funcionarios,
        'empresas': Empresa,
        'departamentos': Departamento,
        'cargos': Cargos,
        'estoque': EstoqueEPI,
        'grade': GradeEPI,
        'equipamentos': ProdutoEPI,
        "estoque_grade": EstoqueGrade
    }

    return model[tipo]

@app.route("/gen_model/<model>", methods = ["GET"])
@login_required
def gen_model(model: str):
    
    str_model = model
    model = getModel(model.lower())
    
    # Extraindo os nomes das colunas do modelo
    
    model.__table__.columns
    columns = []
    for column in model.__table__.columns:
        if not isinstance(column.type, LargeBinary):
            columns.append(column.name)
        
        
    # Criando um DataFrame com as colunas
    df = pd.DataFrame(columns=columns)
    
    # Salvando o DataFrame em uma planilha
    filename = f"{str_model}.xlsx"
    file_path = os.path.join(app.config['TEMP_PATH'], filename)
    
    with pd.ExcelWriter(file_path, engine="auto") as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    
    response = make_response(send_file(f'{file_path}', as_attachment=True))
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@app.route("/import_lotes/<tipo>", methods=["POST"])
@login_required
def import_lotes(tipo: str):

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
            
            try:
                data_admissao = df['data_admissao']
            except:
                data_admissao = None
                
            if data_admissao is not None:
                df['data_admissao'] = pd.to_datetime(
                    df['data_admissao'], errors='coerce')

            data = []
            for _, row in df.iterrows():
                row = row.dropna()
                data_info = row.to_dict()
                
                appends = model(**data_info)
                data.append(appends)
                
            if tipo.lower() == "grade":
                data = []
                for _, row in df.iterrows():
                    data_info = row.to_dict()
                    d = data_info.get("grade")
                    
                    check_entry = model.query.filter_by(grade = d).first()
                    
                    if not check_entry:
                        data_info.update({"grade": str(d)})
                        appends = model(**data_info)
                        data.append(appends)

            db.session.add_all(data)
            db.session.commit()

        flash("Informação cadastrada com sucesso!", "success")
        return redirect(url_for(tipo))

    except Exception as e:
        print(e)
        abort(500)

