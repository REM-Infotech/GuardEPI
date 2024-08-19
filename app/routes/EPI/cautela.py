from flask import jsonify, url_for, render_template, session, abort, flash, request
from flask_login import login_required

from app.Forms import Cautela
from app.models import (RegistrosEPI, ProdutoEPI, EstoqueEPI,
                        Funcionarios, Empresa, EstoqueGrade)

from app.misc import generate_pid
from app.misc.generate_doc import (add_watermark, adjust_image_transparency,
create_EPI_control_sheet, create_watermark_pdf)

import os
from datetime import datetime

from time import sleep
import json

from app import db
from app import app

from app.decorators import read_perm, set_endpoint, create_perm

@app.route("/Cautelas")
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


@app.route('/add-itens', methods=['GET', 'POST'])
@login_required
def add_itens():

    form = Cautela()

    session["itens_lista_cautela"].append(
        [form.nome_epi.data, form.tipo_grade.data, form.qtd_entregar.data])

    item_html = render_template(
        'includes/add_items.html', item=session["itens_lista_cautela"])

    # Retorna o HTML do item
    return item_html


@app.route('/remove-itens', methods=['GET', 'POST'])
@login_required
def remove_itens():

    session["itens_lista_cautela"] = []

    item_html = render_template('includes/add_items.html')

    # Retorna o HTML do item
    return item_html


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
            list_epis_solict = []
            form_flask = list(form.data)
            epi = request.form
            list_epi = list(epi)
            funcionario = form.select_funcionario.data
            nomedoc_cautela = f'Cautela - {funcionario} - {datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.pdf'

            count_cautelas = RegistrosEPI.query.all()
            if not count_cautelas:
                count_cautelas = 1
            else:
                count_cautelas = len(count_cautelas)
            
            epis_lista = []
            valor_calc = 0
            for epis in list_epi:
                if epis not in form_flask and epis != "csrf_token":
                    qtd_entregar = epi[epis].split(" - ")[-1]
                    grade = epi[epis].split(" - ")[1]

                    equip = ProdutoEPI.query.filter_by(nome_epi = epis).first()
                    
                    data_estoque = EstoqueEPI.query.filter(
                        EstoqueEPI.nome_epi == epis).first()
                    estoque_grade = EstoqueGrade.query.filter(
                        EstoqueGrade.nome_epi == epis, 
                        EstoqueGrade.grade == form.tipo_grade.data).first()

                    if estoque_grade:
                        if estoque_grade and estoque_grade.qtd_estoque > 0 and data_estoque.qtd_estoque > 0:
                            
                            list_epis_solict.append([str(data_estoque.id), str(
                                qtd_entregar), data_estoque.nome_epi, grade, equip.ca])
                            estoque_grade.qtd_estoque = estoque_grade.qtd_estoque - 1
                            data_estoque.qtd_estoque = data_estoque.qtd_estoque - 1
                            
                            epis_lista.append(epis)
                            valor_calc = equip.valor_unitario * int(qtd_entregar)

            if len(epis_lista) == 0:
                flash("EPI's sem Estoque", "error")
                return render_template('includes/show_pdf.html', url="")

            to_str = json.dumps(epis_lista).replace("[", "").replace("]", "")
            registrar = RegistrosEPI(
                        nome_epis=to_str,
                        funcionario=funcionario,
                        data_solicitacao=datetime.now(),
                        doc_cautela=nomedoc_cautela,
                        valor_total=valor_calc
                    )

            db.session.add(registrar)
            db.session.commit()

            data_funcionario = Funcionarios.query.filter_by(
                nome_funcionario=funcionario).first()

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
            dbase = Empresa.query.filter(
                Empresa.nome_empresa == data_funcionario.empresa).first()
            image_data = dbase.blob_imagem
            original_path = os.path.join(
                app.config['IMAGE_TEMP_PATH'], "logo.png")
            with open(original_path, 'wb') as file:
                file.write(image_data)

            adjusted_path = os.path.join(
                app.config['Docs_Path'], f"GuardEPI_adjusted{num}.png")
            temp_watermark_pdf = os.path.join(
                app.config['Docs_Path'], f"{num} marca_dagua.pdf")

            try:

                path_cautela = os.path.join(
                    app.config['Docs_Path'], nomedoc_cautela)

                ctrl_sheet = os.path.join(
                    app.config['Docs_Path'], f"EPI_control_sheet{num}.pdf")

                adjust_image_transparency(original_path, adjusted_path, 1)
                create_EPI_control_sheet(ctrl_sheet, employee_data, delivery_data={
                }, item_data=item_data, logo_path=adjusted_path)
                create_watermark_pdf(adjusted_path, temp_watermark_pdf)
                add_watermark(ctrl_sheet, path_cautela, temp_watermark_pdf)
                
                sleep(2)
                
                set_cautela = RegistrosEPI.query.filter_by(
                    doc_cautela=nomedoc_cautela).first()

                if set_cautela is None:
                    url = ""
                    item_html = render_template(
                        'includes/show_pdf.html', url=url)
                    return item_html

                with open(path_cautela, 'rb') as file:
                    cautela_data = file.read()

                set_cautela.blob_cautela = cautela_data
                db.session.commit()

                url = url_for(
                    'serve_pdf', index = set_cautela.id, _external=True, _scheme='https')
                item_html = render_template('includes/show_pdf.html', url=url)
                return item_html

            except Exception as e:
                print(e)
                flash("Erro interno", "error")
                url = ""
                item_html = render_template(
                    'includes/show_pdf.html', url=url)
                return item_html

            finally:

                for root, dirs, files in os.walk(app.config['Docs_Path']):
                    for file in files:
                        if ".pdf" in file or "adjusted" in file:
                            os.remove(f"{root}/{file}")

    except Exception as e:
        print(e)
        flash("Erro interno", "error")
        url = ""
        item_html = render_template(
            'includes/show_pdf.html', url=url)
        return item_html
