import traceback
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from quart import (
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.decorators import create_perm, read_perm
from app.forms import InsertEstoqueForm
from app.misc import format_currency_brl
from app.models import EstoqueEPI, EstoqueGrade, ProdutoEPI, RegistroEntradas

from . import estoque_bp


@estoque_bp.get("/produto")
@login_required
@read_perm
async def produto_epi() -> Response:
    """
    Handles the retrieval and rendering of the stock (Estoque) page.
    This function queries the database for all entries in the EstoqueEPI table,
    prepares the necessary data for rendering the stock page, and returns the
    rendered HTML template. If an error occurs during this process, a 500 error
    is raised with a description of the exception.
    Returns:
        Response: The rendered HTML template for the stock page.
    Raises:
        HTTPException: If an error occurs during the database query or rendering process,
                       a 500 error is raised with the exception description.
    """

    try:
        title = "Estoque Geral (Por Produto)"
        page = "estoque.html"

        database = EstoqueEPI.query.all()

        return await make_response(
            await render_template(
                "index.html",
                page=page,
                title=title,
                database=database,
                format_currency_brl=format_currency_brl,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@estoque_bp.route("/grade", methods=["GET"])
@login_required
@read_perm
async def grade() -> Response:
    """
    Fetches all records from the EstoqueGrade database table and renders the 'estoque_grade.html' page.
    This function queries all entries from the EstoqueGrade table and passes the data to the 'index.html' template
    with 'estoque_grade.html' as the page to be rendered. If an exception occurs during the process, it aborts the
    request with a 500 status code and includes the exception message in the response.
    Returns:
        Response: A Quart response object that renders the 'index.html' template with the specified page and database data.
    Raises:
        HTTPException: If an error occurs during the database query or rendering process, a 500 HTTPException is raised.
    """

    try:
        title = "Estoque Geral (Por Grades)"
        page = "estoque_grade.html"

        database = EstoqueGrade.query.all()

        return await make_response(
            await render_template(
                "index.html",
                page=page,
                database=database,
                title=title,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@estoque_bp.route("/entradas")
@login_required
@read_perm
async def entradas() -> Response:
    try:
        """
        Handles the route for displaying the list of EPI (Personal Protective Equipment) entries.
        This function retrieves all entries from the RegistroEntradas database and renders the
        'index.html' template with the retrieved data, along with the page title and format_currency_brl function.
        Returns:
            str: Rendered HTML template for the EPI entries page.
        """

        title = "Relação de Entradas EPI"
        page = "entradas.html"

        database = RegistroEntradas.query.all()
        return await make_response(
            await render_template(
                "index.html",
                page=page,
                title=title,
                database=database,
                format_currency_brl=format_currency_brl,
            )
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@estoque_bp.route("/lancamento_estoque", methods=["GET", "POST"])
@login_required
@create_perm
async def lancamento_produto() -> Response:
    """
    Handles the product entry process in the inventory system.
    This function performs the following steps:
    1. Validates the form submission.
    2. Checks if the product and its grade already exist in the inventory.
    3. Adds or updates the product and its grade in the inventory.
    4. Records the entry details including the total value and optional invoice file.
    5. Updates the unit value of the product.
    6. Commits the changes to the database.

    Returns:
        Redirects to the inventory page with a success or error message.
    Raises:
        500 Internal Server Error: If any exception occurs during the process.
    """

    try:
        title = "Lançamento de Estoque"
        page = "forms/estoque/estoque_form.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = InsertEstoqueForm()
        if form.validate_on_submit():
            if not form.nota_fiscal.data:
                if form.justificativa.data == "...":
                    await flash(
                        "Inserir nota fiscal ou informar justificativa de estorno!"
                    )
                    return await make_response(redirect(url_for("estoque.produto_epi")))

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

            if form.justificativa.data != "...":
                EntradaEPI.justificativa = form.justificativa.data

            file_nf: FileStorage = form.nota_fiscal.data
            if file_nf:
                file_path = Path(app.config["PDF_TEMP_PATH"]).joinpath(
                    secure_filename(file_nf.filename)
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
            try:
                db.session.commit()
            except errors.UniqueViolation:
                await flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            await flash("Informações salvas com sucesso!", "success")
            return await make_response(redirect(url_for("estoque.produto_epi")))

        if form.errors:
            await flash("Campos Obrigatórios não preenchidos!")
            return await make_response(redirect(url_for("estoque.produto_epi")))

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)
