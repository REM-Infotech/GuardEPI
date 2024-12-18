import os

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from app.decorators import create_perm
from app.forms import InsertEstoqueForm
from app.misc import format_currency_brl
from app.models import EstoqueEPI, EstoqueGrade, ProdutoEPI, RegistroEntradas

from . import epi


@epi.route("/Estoque")
@login_required
def Estoque():
    try:
        database = EstoqueEPI.query.all()
        title = request.endpoint.split(".")[1].capitalize()
        page = "estoque.html"
        form = InsertEstoqueForm()

        return render_template(
            "index.html",
            page=page,
            title=title,
            database=database,
            form=form,
            format_currency_brl=format_currency_brl,
        )
    except Exception as e:
        abort(500, description=str(e))


# Estoque_Grade


@epi.route("/Estoque_Grade", methods=["GET"])
@login_required
def Estoque_Grade():
    try:
        database = EstoqueGrade.query.all()

        page = "estoque_grade.html"

        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@epi.route("/Entradas")
@login_required
def Entradas():
    title = "Relação de Entradas EPI"
    page = "entradas.html"

    database = RegistroEntradas.query.all()
    return render_template(
        "index.html",
        page=page,
        title=title,
        database=database,
        format_currency_brl=format_currency_brl,
    )


@epi.route("/lancamento_estoque", methods=["POST"])
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
