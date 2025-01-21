from functools import wraps
from typing import Any

from flask import abort
from flask import current_app as app
from flask import make_response, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from ..models import Groups, Roles, Routes, Users


def create_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        """
        Função decorada que verifica se o usuário tem permissão para criar.
        Args:
            *args: Argumentos posicionais.
            **kwargs: Argumentos nomeados.
        Returns:
            Any: O resultado da função decorada ou um redirecionamento para a página de login.
        Comportamento:
            - Se o usuário estiver logado e não tiver permissão para criar, retorna um erro 403.
            - Se o usuário não estiver logado, redireciona para a página de login.
            - Caso contrário, executa a função decorada com os argumentos fornecidos.
        """

        user = session.get("username")
        if user:
            if check_permit(user, "CREATE") is False:
                abort(403)

        elif not user:
            return make_response(redirect(url_for("auth.login")))

        return func(*args, **kwargs)

    return decorated_function


def read_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        """
        Função decorada que verifica se o usuário tem permissão para acessar a função decorada.
        Args:
            *args: Argumentos posicionais passados para a função decorada.
            **kwargs: Argumentos nomeados passados para a função decorada.
        Returns:
            Any: O resultado da função decorada, se o usuário tiver permissão.
            Se o usuário não estiver autenticado, redireciona para a página de login.
            Se o usuário não tiver permissão, retorna um erro 403 (Forbidden).
        """

        user = session.get("username")
        if user:
            if check_permit(user, "READ") is False:
                abort(403)

        elif not user:
            return make_response(redirect(url_for("auth.login")))

        return func(*args, **kwargs)

    return decorated_function


def update_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        """
        Função decorada que verifica se o usuário está autenticado e possui permissão para atualizar.
        Args:
            *args: Argumentos posicionais passados para a função decorada.
            **kwargs: Argumentos nomeados passados para a função decorada.
        Returns:
            Any: O resultado da função decorada, ou um redirecionamento para a página de login se o usuário não estiver autenticado,
            ou um erro 403 se o usuário não tiver permissão para atualizar.
        """

        user = session.get("username")
        if user:
            if check_permit(user, "UPDATE") is False:
                abort(403)

        elif not user:
            return make_response(redirect(url_for("auth.login")))

        return func(*args, **kwargs)

    return decorated_function


def delete_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        """
        Função decorada para verificar permissões de usuário antes de executar a função principal.
        Args:
            *args: Argumentos posicionais passados para a função principal.
            **kwargs: Argumentos nomeados passados para a função principal.
        Returns:
            A função principal se o usuário tiver permissão ou estiver autenticado.
            Redireciona para a página de login se o usuário não estiver autenticado.
            Retorna um erro 403 se o usuário não tiver permissão para executar a ação.
        """

        user = session.get("username")
        if user:
            if check_permit(user, "DELETE") is False:

                template = "includes/show.html"
                message = "Você não tem permissões para isto"
                return make_response(render_template(template, message=message))

        elif not user:
            return make_response(redirect(url_for("auth.login")))

        return func(*args, **kwargs)

    return decorated_function


def check_permit(user: str, PERM: str) -> bool:

    db: SQLAlchemy = app.extensions["sqlalchemy"]

    endpoint = f"/{request.blueprint}"

    # user = db.session.query(Users).filter(Users.login == groups_usr).subquery()
    # alias_usr = aliased(user, Users)

    from_groups = (
        db.session.query(Groups)
        .select_from(Users)
        .join(Groups.members)
        .filter(Users.login == user)
        .all()
    )

    for grupo in from_groups:
        for rule in grupo.role:
            route = (
                db.session.query(Routes)
                .select_from(Roles)
                .join(Routes.roles)
                .filter(Roles.id == rule.id)
                .filter(Routes.endpoint == endpoint)
                .first()
            )

            if not route:
                continue

            perm: bool = getattr(route, PERM, False)
            if perm is False:
                continue

            return perm

        # for rule in grupo.role:

        #     end = rule.routes

        #     for route in end:

        #         if route.endpoint != endpoint:
        #             continue

        #         route = route[0]
        #         permit = getattr(route, PERM) is True

        #         return permit

    return False
