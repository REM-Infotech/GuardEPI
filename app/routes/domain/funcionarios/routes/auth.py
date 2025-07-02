import json  # noqa: D100

from flask_sqlalchemy import SQLAlchemy
from quart import Blueprint, Response, jsonify, make_response, request  # noqa: D100
from quart_jwt_extended import create_access_token

from dusdoc_api.app import app
from dusdoc_api.models.users.funcionarios import Funcionarios as Users

auth = Blueprint(__name__.replace(".", "_"), __name__, url_prefix="/auth_funcionario")


@auth.route("/login", methods=["GET", "POST"])
async def login() -> Response:
    """Handle user login."""
    data = await request.form or await request.data or await request.json
    if isinstance(data, bytes):
        data = data.decode()

    if isinstance(data, str):
        data = json.loads(data)

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    user = db.session.query(Users).filter(Users.email == data.get("email")).first()

    if user and user.check_password(data.get("password")):
        return await make_response(
            jsonify({
                "message": "Login efetuado com sucesso!",
                "token": create_access_token(identity=user),
            }),
            200,
        )

    return await make_response(
        jsonify({
            "message": "Usuário/Senha Incorretos!",
        }),
        401,
    )
