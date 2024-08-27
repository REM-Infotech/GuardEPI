from flask import (jsonify, url_for, render_template, 
                   session, abort, flash, request, get_flashed_messages)
from flask_login import login_required

from app.Forms import Cautela
from app.models import (RegistrosEPI, ProdutoEPI, EstoqueEPI, RegistroSaidas,
                        Funcionarios, Empresa, EstoqueGrade)

from app.misc import generate_pid
from app.misc.generate_doc import (add_watermark, adjust_image_transparency,
create_EPI_control_sheet, create_watermark_pdf)

import os
import uuid
from datetime import datetime

from time import sleep
import json

from app import db
from app import app

from app.misc import format_currency_brl
from app.decorators import read_perm, set_endpoint, create_perm

@app.before_request
def setgroups():
    
    if request.endpoint == "Cautelas":
        if not session.get("uuid_Cautelas", None):
            
            session["uuid_Cautelas"] = str(uuid.uuid4())
            pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Cautelas"]}.json")
            
            if os.path.exists(pathj):
                os.remove(pathj)
            
            json_obj = json.dumps([])
            
            with open(pathj, 'w') as f:
                f.write(json_obj)
                
@app.route('/add_itens', methods=['GET', 'POST'])
@login_required
def add_itens():
    
    form = Cautela()
    list = [form.nome_epi.data, form.tipo_grade.data, form.qtd_entregar.data]

    pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Cautelas"]}.json")
    
    with open(pathj, 'rb') as f:
        list_groups = json.load(f)

    list_groups.append(list)
    json_obj = json.dumps(list_groups)
        
    with open(pathj, 'w') as f:
        f.write(json_obj)

    item_html = render_template(
        'includes/add_items.html', item=list_groups)

    # Retorna o HTML do item
    return item_html


@app.route('/remove-itens', methods=['GET', 'POST'])
@login_required
def remove_itens():
    
    pathj = os.path.join(app.config['TEMP_PATH'], f"{session["uuid_Cautelas"]}.json")
    json_obj = json.dumps([])
    
    with open(pathj, 'w') as f:
        f.write(json_obj)
        
    item_html = render_template('includes/add_itens.html')
    return item_html

@app.route("/Registro_Saidas", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Registro_Saidas():
    
    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = RegistroSaidas.query.all()
    title = request.endpoint.capitalize().replace("_", " ")
    DataTables = 'js/DataTables/DataTables.js'
    return render_template("index.html", page=page, title=title, database=database, 
                           DataTables=DataTables, format_currency_brl=format_currency_brl)

@app.route("/Cautelas", methods = ["GET"])
@login_required
@set_endpoint
@read_perm
def Cautelas():

    page = f"pages/epi/{request.endpoint.lower()}.html"
    database = RegistrosEPI.query.all()
    title = request.endpoint.capitalize()
    DataTables = 'js/DataTables/epi/CautelasTable.js'
    form = Cautela()
    session["itens_lista_cautela"] = []
    return render_template("index.html", page=page, title=title, database=database, 
                           DataTables=DataTables, form=form)

@app.route("/get-grade", methods=["POST"])
@login_required
def get_grade():

    try:
        form = Cautela()
        lista = []
        dbase = EstoqueGrade.query.filter_by(nome_epi=form.nome_epi.data).all()
        for query in dbase:
            lista.append((query.grade, query.grade))
        form.tipo_grade.choices.extend(lista)

        page = 'pages/forms/cautelas/get_grade.html'
        return render_template(page, form=form)
    except Exception as e:
        pass


@app.route("/emitir_cautela", methods=["POST"])
@login_required
@create_perm
def emitir_cautela():

    try:
        form = Cautela()
        if form.validate_on_submit:
            
            ## Lista EPI Solicitadas
            list_epis_solict = []
            para_registro = []
            ## Lista Itens Flask Form
            form_flask = list(form.data)
            
            ## Itens formulário Avulso (Sem Flask Form)
            epi = request.form
            list_epi = list(epi)
            
            ## Query Funcionário
            funcionario = form.select_funcionario.data
            data_funcionario = Funcionarios.query.filter_by(
                nome_funcionario=funcionario).first()
            
            ## Query Empresa
            dbase = Empresa.query.filter(
                Empresa.nome_empresa == data_funcionario.empresa).first()
            
            if not dbase:
                
                flash("Empresa não cadastrada!", "error")   
                sleep(1)
                messages = get_flashed_messages()
                return render_template('includes/show_pdf.html', url="", messages=messages)
                    
            nomefilename = f'Cautela - {funcionario} - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.pdf'
            count_cautelas = RegistrosEPI.query.all()
            if not count_cautelas:
                count_cautelas = 1
            else:
                count_cautelas = len(count_cautelas)
            
            epis_lista = []
            valor_calc = 0
            
            for epi_solicitada in list_epi:
                if epi_solicitada not in form_flask and epi_solicitada != "csrf_token":
                    
                    qtd_entregar = epi[epi_solicitada].split(" - ")[-1]
                    grade = epi[epi_solicitada].split(" - ")[1]

                    equip = ProdutoEPI.query.filter_by(nome_epi = epi_solicitada).first()
                    
                    ## Query Estoque geral
                    data_estoque = EstoqueEPI.query.filter(EstoqueEPI.nome_epi == epi_solicitada).first()
                    
                    ## Query Estoque Grades
                    estoque_grade = EstoqueGrade.query.filter(EstoqueGrade.nome_epi == epi_solicitada, 
                        EstoqueGrade.grade == form.tipo_grade.data).first()

                    
                    if estoque_grade:
                        if estoque_grade and estoque_grade.qtd_estoque > 0 and data_estoque.qtd_estoque > 0:
                            
                            list_epis_solict.append([str(data_estoque.id), str(qtd_entregar), data_estoque.nome_epi, grade, equip.ca])
                            estoque_grade.qtd_estoque = estoque_grade.qtd_estoque - 1
                            data_estoque.qtd_estoque = data_estoque.qtd_estoque - 1
                            
                            epis_lista.append(epi_solicitada)
                            
                            para_registro.append(RegistroSaidas(
                                
                                nome_epi=epi_solicitada,
                                qtd_saida=int(qtd_entregar),
                                valor_total = equip.valor_unitario * int(qtd_entregar)
                                
                            ))
                            
                            valor_calc = equip.valor_unitario * int(qtd_entregar)

            if len(epis_lista) == 0:
                flash("EPI's sem Estoque", "error")
                sleep(1)
                messages = get_flashed_messages()
                return render_template('includes/show_pdf.html', url="", messages=messages)
            
            to_str = json.dumps(epis_lista).replace("[", "").replace("]", "")
            registrar = RegistrosEPI(
                        nome_epis=to_str.encode('utf-8').decode('unicode_escape'),
                        funcionario=funcionario,
                        data_solicitacao=datetime.now(),
                        filename=nomefilename,
                        valor_total=valor_calc
                    )

            
            db.session.add(registrar)
            db.session.add_all(para_registro)
            db.session.commit()

            employee_data = {
                'company': data_funcionario.empresa,
                'name': data_funcionario.nome_funcionario,
                'cargo': data_funcionario.cargo,
                'departamento': data_funcionario.departamento,
                'registration': data_funcionario.codigo,
                'lancamento_code': str(count_cautelas+1).zfill(6)
            }

            item_data = [
                ["ID", "Qtde", "Descrição", "Grade", "CA"],
            ]

            for obj in list_epis_solict:

                item_data.append(obj)

            num = generate_pid()
            
            image_data = dbase.blob_doc
            original_path = os.path.join(
                app.config['IMAGE_TEMP_PATH'], "logo.png")
            with open(original_path, 'wb') as file:
                file.write(image_data)

            adjusted_path = os.path.join(
                app.config['DOCS_PATH'], f"GuardEPI_adjusted{num}.png")
            temp_watermark_pdf = os.path.join(
                app.config['DOCS_PATH'], f"{num} marca_dagua.pdf")

            try:

                path_cautela = os.path.join(
                    app.config['DOCS_PATH'], nomefilename)

                ctrl_sheet = os.path.join(
                    app.config['DOCS_PATH'], f"EPI_control_sheet{num}.pdf")

                adjust_image_transparency(original_path, adjusted_path, 1)
                create_EPI_control_sheet(ctrl_sheet, employee_data, delivery_data={
                }, item_data=item_data, logo_path=adjusted_path)
                create_watermark_pdf(adjusted_path, temp_watermark_pdf)
                add_watermark(ctrl_sheet, path_cautela, temp_watermark_pdf)
                
                sleep(2)
                
                set_cautela = RegistrosEPI.query.filter_by(
                    filename=nomefilename).first()

                if set_cautela is None:
                    url = ""
                    item_html = render_template(
                        'includes/show_pdf.html', url=url)
                    return item_html

                with open(path_cautela, 'rb') as file:
                    cautela_data = file.read()

                set_cautela.blob_doc = cautela_data
                db.session.commit()

                url = url_for(
                    'serve_pdf', index = set_cautela.id, md="Cautelas", _external=True, _scheme='https')
                item_html = render_template('includes/show_pdf.html', url=url)
                return item_html

            except Exception as e:
                flash("Erro interno", "error")
                sleep(1)
                messages = get_flashed_messages()
                return render_template('includes/show_pdf.html', url="", messages=messages)

    except Exception as e:
        print(e)
        flash("Erro interno", "error")
        sleep(1)
        messages = get_flashed_messages()
        return render_template('includes/show_pdf.html', url="", messages=messages)
