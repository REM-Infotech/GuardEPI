import json
import traceback  # traceback
from pathlib import Path
from typing import Dict, List

from flask import Response, abort
from flask import current_app as app
from flask import flash, make_response, redirect, render_template, session
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy

from app.decorators import create_perm, read_perm

from ...forms import FormRoles
from ...models import Groups, Roles, Routes
from . import config


@config.route("/add_itens", methods=["GET", "POST"])
@login_required
@read_perm
def add_itens() -> Response:

    try:

        form = FormRoles()

        rota = form.rota
        regras = form.permissoes

        item_role: Dict[str, str | Dict[str, bool]] = {
            "ROTA": rota.data,
            "REGRAS": {},
        }

        item_role.get("REGRAS").update({regra: True for regra in regras.data})

        hex_name_json = session["json_filename"]
        path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
        json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

        with json_file.open("rb") as f:
            list_roles: list[Dict[str, str | Dict[str, bool]]] = json.load(f)

        item_role.update({"ID": len(list_roles)})

        list_roles.append(item_role)
        json_obj = json.dumps(list_roles)

        with json_file.open("w") as f:
            f.write(json_obj)

        to_view: List[Dict[str, str]] = []

        for item in list_roles:
            keys = item_role.get("REGRAS").keys()
            dict_to_view = {
                "ID": item.get("ID"),
                "ROTA": item.get("ROTA"),
                "REGRAS": " - ".join(keys),
            }

            to_view.append(dict_to_view)
        # Retorna o HTML do item
        return make_response(
            render_template("forms/roles/add_items.html", item=to_view)
        )
    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/remove-itens", methods=["GET", "POST"])
@login_required
@read_perm
def remove_itens() -> Response:

    try:
        hex_name_json = session["json_filename"]
        path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
        json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()
        list_roles = None

        with json_file.open("w") as f:
            f.write(json.dumps([]))

        item_html = render_template("forms/roles/add_items.html", item=list_roles)
        return make_response(item_html)

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/roles", methods=["GET"])
@login_required
@read_perm
def roles() -> Response:
    try:

        title = "Regras"
        page = "roles.html"
        database = Roles.query.all()

        return make_response(
            render_template("index.html", title=title, database=database, page=page)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.route("/cadastro_regra", methods=["GET", "POST"])
@login_required
@create_perm
def cadastro_regra() -> Response:

    try:
        """
        Handles the creation of a new group.
        Renders a form for creating a new group and processes the form submission.
        If the form is valid and the group does not already exist, a new group is created
        and added to the database along with its members.

        Returns:
            - On successful group creation, redirects to the Roles configuration page.
            - On form validation failure or if the group already exists, re-renders the form with an error message.
        """

        form = FormRoles()
        title = "Criar Regra"
        page = "forms/roles/FormRoles.html"

        if form.validate_on_submit():

            db: SQLAlchemy = app.extensions["sqlalchemy"]
            rulename = form.name_rule.data
            query = db.session.query(Roles).filter(Roles.name_role == rulename).first()

            routes_add = []

            if query:
                flash("Regra já existente!", "error")
                return make_response(
                    render_template("index.html", page=page, form=form, title=title)
                )

            new_ruleset = Roles(
                name_role=rulename,
                description=form.desc.data,
            )

            for group in form.grupos.data:

                grp = (
                    db.session.query(Groups).filter(Groups.name_group == group).first()
                )
                new_ruleset.groups.append(grp)

            hex_name_json = session["json_filename"]
            path_json = Path(app.config["TEMP_PATH"]).joinpath(hex_name_json).resolve()
            json_file = path_json.joinpath(hex_name_json).with_suffix(".json").resolve()

            with json_file.open("rb") as f:
                list_roles: list[Dict[str, str | Dict[str, bool]]] = json.load(f)

            keys_routes = {}

            for key in Routes.__dict__.keys():
                if key in ["CREATE", "READ", "UPDATE", "DELETE"]:
                    keys_routes.update({key: False})

            for item in list_roles:
                to_add = keys_routes
                list_items = list(item.items())
                for key, value in list_items:
                    if key == "ROTA":
                        to_add.update({"endpoint": value})
                        continue

                    if key == "REGRAS":

                        rules = list(value.items())
                        for key_, value_ in rules:
                            to_add.update({key_: value_})

                end_cfg = Routes(**to_add)
                end_cfg.roles.append(new_ruleset)
                routes_add.append(end_cfg)

            db.session.add(new_ruleset)
            db.session.add_all(routes_add)

            db.session.commit()

            session.pop("json_filename")

            flash("Regra criada com sucesso")
            return make_response(redirect("/config/roles"))

        return make_response(
            render_template("index.html", page=page, form=form, title=title)
        )

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


@config.get("/deletar_regra/<int:id>")
@login_required
def deletar_regra(id: int) -> Response:

    try:
        db: SQLAlchemy = app.extensions["sqlalchemy"]

        from_groups = (
            db.session.query(Groups)
            .select_from(Roles)
            .join(Roles.groups)
            .filter(Roles.id == id)
            .all()
        )

        from_routes = (
            db.session.query(Routes)
            .select_from(Roles)
            .join(Roles.route)
            .filter(Roles.id == id)
            .all()
        )

        role = db.session.query(Roles).filter(Roles.id == id).first()

        for route in from_routes:

            db.session.delete(route)

        for group in from_groups:
            group.role.remove(role)

        db.session.delete(role)
        db.session.commit()

        message = "Regra deletada com sucesso!"
        template = "includes/show.html"

    except Exception:

        app.logger.exception(traceback.format_exc())

        message = "Erro ao deletar regra"
        template = "includes/show.html"

    return make_response(render_template(template, message=message))
