import json
from functools import wraps

from flask import abort, redirect, request, session, url_for

from app.models import Permissions


def set_endpoint(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pragma: no cover
        session["endpoint"] = request.endpoint
        return func(*args, **kwargs)

    return decorated_function  # pragma: no cover


def create_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pragma: no cover
        group_usr = session.get("groups_usr", None)
        if group_usr:
            if check_permit(group_usr, "CREATE") is False:
                abort(403)

        return func(*args, **kwargs)

    return decorated_function  # pragma: no cover


def read_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pragma: no cover
        group_usr = session.get("groups_usr", None)
        if group_usr:
            if check_permit(group_usr, "READ") is False:
                abort(403)

        return func(*args, **kwargs)

    return decorated_function  # pragma: no cover


def update_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pragma: no cover
        group_usr = session.get("groups_usr", None)
        if group_usr:
            if check_permit(group_usr, "UPDATE") is False:
                abort(403)

        return func(*args, **kwargs)

    return decorated_function  # pragma: no cover


def delete_perm(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):  # pragma: no cover
        group_usr = session.get("groups_usr", None)
        if group_usr:
            if check_permit(group_usr, "DELETE") is False:
                abort(403)

        return func(*args, **kwargs)

    return decorated_function  # pragma: no cover


def check_permit(groups_usr: list, PERM: str) -> bool:  # pragma: no cover
    if session.get("username") == "root":
        return True

    end = session.get("endpoint", None)

    if not end:
        return redirect(url_for("dash.dashboard"))

    for grp in groups_usr:
        rules = Permissions.query.all()

        for rule in rules:
            if any(
                grp == grupo_membro for grupo_membro in json.loads(rule.groups_members)
            ):
                perms = json.loads(rule.perms)
                for rota in perms:
                    grant = perms[rota]
                    if any(PERM == perms and rota == end for perms in grant):
                        return True

    return False
