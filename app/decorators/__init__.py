from functools import wraps

from flask import current_app as app
from flask import abort, redirect, session, url_for, request
from typing import Any

from flask_sqlalchemy import SQLAlchemy

from ..models import Users

# from app.models import Permissions


def create_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        user = session.get("username")
        if user:
            if check_permit(user, "CREATE") is False:
                abort(403)

        elif not user:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function


def read_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        user = session.get("username")
        if user:
            if check_permit(user, "READ") is False:
                abort(403)

        elif not user:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function


def update_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs) -> Any:
        user = session.get("username")
        if user:
            if check_permit(user, "UPDATE") is False:
                abort(403)

        elif not user:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function


def delete_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = session.get("username")
        if user:
            if check_permit(user, "DELETE") is False:
                abort(403)

        elif not user:
            return redirect(url_for("auth.login"))

        return func(*args, **kwargs)

    return decorated_function


def check_permit(groups_usr: list, PERM: str) -> bool:

    return True
    # db: SQLAlchemy = app.extensions["sqlalchemy"]

    # endpoint = f"/{request.blueprint}"

    # user = db.session.query(Users).filter(Users.login == groups_usr).first()

    # for grupo in user.group:
    #     for rule in grupo.role:

    #         end = rule.routes

    #         for route in end:

    #             if route.endpoint != endpoint:
    #                 continue

    #             route = route[0]
    #             permit = getattr(route, PERM) is True

    #             return permit

    # return False
