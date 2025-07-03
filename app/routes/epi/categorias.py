import traceback

from flask_sqlalchemy import SQLAlchemy
from psycopg2 import errors
from quart import (
    Response,
    abort,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from quart import current_app as app
from quart_auth import login_required

from app.decorators import create_perm, delete_perm, read_perm, update_perm
from app.forms import FormCategorias
from app.models import ClassesEPI

from . import epi


@epi.route("/categorias", methods=["GET"])
@login_required
@read_perm
async def categorias() -> Response:
    try:
        """
        Renders the 'categorias' page with data from the ClassesEPI database.
        This function queries all entries from the ClassesEPI database and passes
        the data to the 'index.html' template along with the page name 'categorias.html'.
        Returns:
            A rendered HTML template with the page name and database entries.
        """

        title = "Categorias"
        page = "categorias.html"
        database = ClassesEPI.query.all()

        return await make_response(
            await render_template(
                "index.html", page=page, database=database, title=title
            )
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/categorias/cadastrar", methods=["GET", "POST"])
@login_required
@create_perm
async def cadastrar_categoria() -> Response:
    try:
        """
        Handles the creation of a new category.
        This function processes the form submission for creating a new category.
        It validates the form data, adds the new category to the database, and
        provides feedback to the user.
        Returns:
            Response: A redirect to the categories page if the form is successfully
            submitted and processed, or renders the form template with the appropriate
            context if the form is not submitted or is invalid.
        """

        endpoint = "Categoria"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        form = FormCategorias()

        db: SQLAlchemy = app.extensions["sqlalchemy"]

        if form.validate_on_submit():
            to_add = {}
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key.lower() == "csrf_token" or key.lower() == "submit":
                    continue

                to_add.update({key: value})

            item = ClassesEPI(**to_add)
            db.session.add(item)
            try:
                db.session.commit()
            except errors.UniqueViolation:
                await flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            await flash("Categoria cadastrada com sucesso!", "success")
            return await make_response(
                make_response(redirect(url_for("epi.categorias")))
            )

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
@update_perm
async def editar_categoria(id) -> Response:
    try:
        """
        Edit an existing category based on the provided ID.
        This function handles both GET and POST requests. On a GET request, it populates
        the form with the existing category data. On a POST request, it validates the form
        and updates the category in the database if the form is valid.
        Args:
            id (int): The ID of the category to be edited.
        Returns:
            Response: Renders the form template on GET request or redirects to the categories
            list on successful form submission.
        """

        endpoint = "Categoria"
        act = "Cadastro"

        title = " ".join([act, endpoint])
        page = "form_base.html"

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        form = FormCategorias()

        classe = db.session.query(ClassesEPI).filter(ClassesEPI.id == id).first()

        if request.method == "GET":
            form = FormCategorias(**classe.__dict__)

        if form.validate_on_submit():
            form_data = form.data
            list_form_data = list(form_data.items())

            for key, value in list_form_data:
                if key != "csrf_token" or key != "submit" and value:
                    setattr(classe, key, value)

            try:
                db.session.commit()
            except errors.UniqueViolation:
                await flash("Item com informações duplicadas!")
                return await make_response(
                    await render_template(
                        "index.html", page=page, form=form, title=title
                    )
                )

            await flash("Categoria editada com sucesso!", "success")
            return await make_response(redirect(url_for("epi.categorias")))

        return await make_response(
            await render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@epi.post("/categorias/deletar/<int:id>")
@login_required
@delete_perm
async def deletar_categoria(id: int) -> Response:
    try:
        """
        Deletes a category from the database based on the provided ID.
        Args:
            id (int): The ID of the category to be deleted.
        Returns:
            Response: A rendered template with a success message.
        Raises:
            sqlalchemy.orm.exc.NoResultFound: If no category with the given ID is found.
        """

        db: SQLAlchemy = app.extensions["sqlalchemy"]
        classe = db.session.query(ClassesEPI).filter(ClassesEPI.id == id).first()

        db.session.delete(classe)
        db.session.commit()

        template = "includes/show.html"
        message = "Informação deletada com sucesso!"
        return await make_response(await render_template(template, message=message))

    except Exception:
        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar regra"
        template = "includes/show.html"

    return await make_response(await render_template(template, message=message))
