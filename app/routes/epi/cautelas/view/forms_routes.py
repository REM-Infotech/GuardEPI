from flask_sqlalchemy import SQLAlchemy
from quart import (
    Response,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from quart_auth import login_required
from werkzeug.datastructures import MultiDict

from app.decorators import create_perm
from app.forms.epi import CancelarCautelaForm, FormEnvioCautelaAssinada
from app.models.EPI.cautelas import RegistrosEPI
from app.routes.epi import estoque_bp
from app.routes.epi.cautelas.actions import add_cautela_assinada, cancelamento_cautela


@estoque_bp.route("/envio_cautela_assinada/<int:id_cautela>", methods=["GET", "POST"])
@login_required
@create_perm
async def envio_cautela_assinada(id_cautela: int) -> Response:
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]

    query = db.session.query(RegistrosEPI).filter_by(id=id_cautela).first()

    list_items_data = [
        ("nome_funcionario", query.funcionario),
        ("nome_cautela", query.filename),
    ]

    if request.method == "POST":
        fm = await request.form
        files = await request.files
        if not fm.get("confirm_form"):
            await flash("É necessário aceitar os termos do formulário")
            return await make_response(redirect(url_for("estoque.cautelas")))

        files_data = dict(list(files.items()))
        form_data = dict(list(fm.items()))

        list_items_data.extend(list(form_data.items()))
        list_items_data.extend(list(files_data.items()))

    data = MultiDict(list_items_data)

    form = FormEnvioCautelaAssinada(formdata=data)
    url_action = request.full_path

    if form.validate_on_submit():
        await add_cautela_assinada(form, query, db)

        await flash("Cautela assinada salva com sucesso!", "success")
        return await make_response(redirect(url_for("estoque.cautelas")))

    if request.method == "GET":
        return await make_response(
            await render_template(
                "forms/envio_assinado.html",
                form=form,
                url_action=url_action,
            )
        )

    return await make_response(redirect(url_for("estoque.cautelas")))


@estoque_bp.route("/cancelar_cautela/<int:id_cautela>", methods=["GET", "POST"])
@login_required
@create_perm
async def cancelar_cautela(id_cautela: int) -> Response:
    db: SQLAlchemy = current_app.extensions["sqlalchemy"]
    query = db.session.query(RegistrosEPI).filter_by(id=id_cautela).first()

    list_items_data = [
        ("nome_funcionario", query.funcionario),
        ("nome_cautela", query.filename),
    ]

    if request.method == "POST":
        fm = await request.form

        if not fm.get("confirm_form"):
            await flash("É necessário aceitar os termos do formulário")
            return await make_response(redirect(url_for("estoque.cautelas")))

        form_data = dict(list(fm.items()))
        list_items_data.extend(list(form_data.items()))

    data = MultiDict(list_items_data)

    form = CancelarCautelaForm(formdata=data)
    url_action = request.full_path

    if form.validate_on_submit():
        await cancelamento_cautela(db, id_cautela)
        await flash("Cautela cancelada com sucesso!", "success")

    if request.method == "GET":
        return await make_response(
            await render_template(
                "forms/cancelar_cautela.html",
                form=form,
                url_action=url_action,
            )
        )

    return await make_response(redirect(url_for("estoque.cautelas")))
