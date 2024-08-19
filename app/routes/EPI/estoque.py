from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app
from app import db
from app.models import (RegistroEntradas, EstoqueEPI, EstoqueGrade)
from app.Forms import IMPORTEPIForm
from app.Forms import InsertEstoqueForm

from app.misc import format_currency_brl
from app.decorators import read_perm, set_endpoint, create_perm

import os


@app.route("/Estoque")
@login_required
@set_endpoint
@read_perm
def Estoque():

    database = EstoqueEPI.query.all()
    title = request.endpoint.capitalize()
    DataTables = 'js/DataTables/epi/EstoqueTable.js'
    page = f"pages/epi/{request.endpoint.lower()}.html"
    form = InsertEstoqueForm()

    importForm = IMPORTEPIForm()
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, form=form, importForm=importForm,
                           format_currency_brl=format_currency_brl)

## Estoque_Grade    
@app.route("/Estoque_Grade", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Estoque_Grade():
    
    database = EstoqueGrade.query.all()
    DataTables = f'js/DataTables/epi/{request.endpoint.lower()}.js'
    page = f"pages/epi/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, DataTables=DataTables,
                           database = database)
    
@app.route("/Entradas")
@login_required
@set_endpoint
@read_perm
def Entradas():

    title = "Relação de Entradas EPI"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    importForm = IMPORTEPIForm()
    database = RegistroEntradas.query.all()
    DataTables = 'js/DataTables/epi/entradas.js'
    return render_template("index.html", page=page, title=title, database=database,
                           DataTables=DataTables, importForm=importForm,
                           format_currency_brl=format_currency_brl)
    
@app.route("/lancamento_estoque", methods=["POST"])
@login_required
@create_perm
def lancamento_produto():
    
    form = InsertEstoqueForm()
    if form.validate_on_submit():
        
        query_Estoque = EstoqueEPI.query
        query_EstoqueGrade = EstoqueGrade.query
        
        dbase_1 = query_EstoqueGrade.filter_by(nome_epi = form.nome_epi.data, 
                                               grade = form.tipo_grade.data).first()
        dbase_2 = query_Estoque.filter_by(nome_epi = form.nome_epi.data).first()
        
        if not dbase_1:
            cad_1 = EstoqueGrade(
                nome_epi=form.nome_epi.data,
                tipo_qtd=form.tipo_qtd.data,
                qtd_estoque=form.qtd_estoque.data,
                grade=form.tipo_grade.data)
            
            db.session.add(cad_1)
            if not dbase_2:
                cad_2 = EstoqueEPI(
                    nome_epi=form.nome_epi.data,
                    tipo_qtd=form.tipo_qtd.data,
                    qtd_estoque=form.qtd_estoque.data
                )
                
                db.session.add(cad_2)
            else:
                dbase_2.qtd_estoque = dbase_2.qtd_estoque + form.qtd_estoque.data
                
        else:
            dbase_1.qtd_estoque = dbase_1.qtd_estoque + form.qtd_estoque.data
            if not dbase_2:
                cad_2 = EstoqueEPI(
                    nome_epi=form.nome_epi.data,
                    tipo_qtd=form.tipo_qtd.data,
                    qtd_estoque=form.qtd_estoque.data
                )
                db.session.add(cad_2)
            else:
                dbase_2.qtd_estoque = dbase_2.qtd_estoque + form.qtd_estoque.data
        
        file_nf = form.nota_fiscal.data
        
        file_path = os.path.join(app.config['PDF_TEMP_PATH'], secure_filename(file_nf.filename))
        file_nf.save(file_path)
        with open(file_path, 'rb') as f:
            blob_doc = f.read()
        data_insert = float(str(form.valor_total.data).replace(
        "R$ ", "").replace(".", "").replace(",", "."))
        EntradaEPI = RegistroEntradas(
            nome_epi = form.nome_epi.data,
            grade=form.tipo_grade.data,
            tipo_qtd=form.tipo_qtd.data,
            qtd_entrada=form.qtd_estoque.data,
            nota_fiscal = secure_filename(file_nf.filename),
            blob_nota_fiscal = blob_doc,
            valor_total=data_insert)
        
        db.session.add(EntradaEPI)        
        db.session.commit()
        
        flash("Informações salvas com sucesso!", "success")
        return redirect(url_for('Estoque'))

