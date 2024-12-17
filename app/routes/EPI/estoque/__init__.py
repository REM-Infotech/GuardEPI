import os
from pathlib import Path

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.decorators import create_perm, read_perm, set_endpoint
from app.forms import IMPORTEPIForm, InsertEstoqueForm
from app.misc import format_currency_brl
from app.models import EstoqueEPI, EstoqueGrade, ProdutoEPI, RegistroEntradas

template_folder = Path(__file__).parent.resolve().joinpath("templates")
estoque = Blueprint("estoque", __name__, template_folder=template_folder)


@estoque.route("/Estoque")
@login_required
@set_endpoint
@read_perm
def Estoque():
    try:
        database = EstoqueEPI.query.all()
        title = request.endpoint.capitalize()
        DataTables = "js/DataTables/epi/EstoqueTable.js"
        page = f"pages/epi/{request.endpoint.lower()}.html"
        form = InsertEstoqueForm()

        importForm = IMPORTEPIForm()
        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            DataTables=DataTables,
            form=form,
            importForm=importForm,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))


# Estoque_Grade


@estoque.route("/Estoque_Grade", methods=["GET"])
@login_required
@set_endpoint
@read_perm
def Estoque_Grade():
    try:
        database = EstoqueGrade.query.all()
        DataTables = f"js/DataTables/epi/{request.endpoint.lower()}.js"
        page = f"pages/epi/{request.endpoint.lower()}.html"
        importForm = IMPORTEPIForm()
        return render_template(
            "index.html",
            page=page,
            DataTables=DataTables,
            database=database,
            importForm=importForm,
        )
    except Exception as e:
        abort(500, description=str(e))


@estoque.route("/Entradas")
@login_required
@set_endpoint
@read_perm
def Entradas():
    title = "Relação de Entradas EPI"
    page = f"pages/epi/{request.endpoint.lower()}.html"
    importForm = IMPORTEPIForm()
    database = RegistroEntradas.query.all()
    DataTables = "js/DataTables/epi/entradas.js"
    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        DataTables=DataTables,
        importForm=importForm,
        format_currency_brl=format_currency_brl,
    )


@estoque.route("/lancamento_estoque", methods=["POST"])
@login_required
@create_perm
def lancamento_produto():
    try:
        form = InsertEstoqueForm()
        if form.validate_on_submit():
            query_Estoque = EstoqueEPI.query
            query_EstoqueGrade = EstoqueGrade.query

            dbase_1 = query_EstoqueGrade.filter_by(
                nome_epi=form.nome_epi.data, grade=form.tipo_grade.data
            ).first()
            dbase_2 = query_Estoque.filter_by(nome_epi=form.nome_epi.data).first()

            if not dbase_1:
                cad_1 = EstoqueGrade(
                    nome_epi=form.nome_epi.data,
                    tipo_qtd=form.tipo_qtd.data,
                    qtd_estoque=form.qtd_estoque.data,
                    grade=form.tipo_grade.data,
                )

                db.session.add(cad_1)
                if not dbase_2:
                    cad_2 = EstoqueEPI(
                        nome_epi=form.nome_epi.data,
                        tipo_qtd=form.tipo_qtd.data,
                        qtd_estoque=form.qtd_estoque.data,
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
                        qtd_estoque=form.qtd_estoque.data,
                    )
                    db.session.add(cad_2)
                else:
                    dbase_2.qtd_estoque = dbase_2.qtd_estoque + form.qtd_estoque.data

            data_insert = float(
                str(form.valor_total.data)
                .replace("R$ ", "")
                .replace(".", "")
                .replace(",", ".")
            )

            # Registro da Entrada
            EntradaEPI = RegistroEntradas(
                nome_epi=form.nome_epi.data,
                grade=form.tipo_grade.data,
                tipo_qtd=form.tipo_qtd.data,
                qtd_entrada=form.qtd_estoque.data,
                valor_total=data_insert,
            )

            file_nf = form.nota_fiscal.data
            if file_nf:
                file_path = os.path.join(
                    app.config["PDF_TEMP_PATH"], secure_filename(file_nf.filename)
                )
                file_nf.save(file_path)
                with open(file_path, "rb") as f:
                    blob_doc = f.read()
                EntradaEPI.filename = secure_filename(file_nf.filename)
                EntradaEPI.blob_doc = blob_doc

            new_valor_unitario = data_insert // form.qtd_estoque.data
            dbase_produto = ProdutoEPI.query.filter_by(
                nome_epi=form.nome_epi.data
            ).first()
            dbase_produto.valor_unitario = new_valor_unitario

            db.session.add(EntradaEPI)
            db.session.commit()

            flash("Informações salvas com sucesso!", "success")
            return redirect(url_for("Estoque"))

        if form.errors:
            flash("Campos Obrigatórios não preenchidos!")
            return redirect(url_for("Estoque"))

    except Exception as e:
        abort(500, description=str(e))
