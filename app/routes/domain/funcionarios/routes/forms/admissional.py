# noqa: D100
import json

from flask_sqlalchemy import SQLAlchemy
from quart import Response, current_app, jsonify, make_response, request
from quart.datastructures import FileStorage
from quart.views import MethodView
from werkzeug.datastructures import CombinedMultiDict, MultiDict  # noqa: F401

from dusdoc_api.models.admissional import FileModel, FormAdmissional, RegistryAdmissao
from dusdoc_api.models.users.funcionarios import Funcionarios


class AdmissionalFormView(MethodView):  # noqa: D101
    init_every_request = False
    methods = ["GET", "POST"]

    def __init__(self, model: Funcionarios) -> None:  # noqa: D107
        self.model = model

    async def post(self, _id: str) -> Response:  # noqa: ANN003, ANN201
        db: SQLAlchemy = current_app.extensions["sqlalchemy"]
        files = await request.files
        files: dict[str, FileStorage] = dict(list(files.items()))
        data = await request.data or await request.form or await request.json

        if isinstance(data, bytes):
            data = data.decode()
            if isinstance(data, str):
                data = json.loads(data)

        data = dict(list(data.items()))
        # Remove 'id' if present to avoid datatype mismatch
        if isinstance(data, dict) and "id" in data:
            data.pop("id")

        to_add = []

        with db.session.no_autoflush:
            registryAdmissional = (  # noqa: N806
                db.session.query(RegistryAdmissao)
                .filter(
                    RegistryAdmissao.funcionario_id == _id,
                )
                .first()
            )

            registryAdmissional.funcionario.status_admissao = "AGUARDANDO ANÁLISE"
            newAdmissao = FormAdmissional(**data)  # noqa: N806
            newAdmissao.submited = True

            for k, v in list(files.items()):
                file_model = FileModel(
                    filename=k,
                    secondary_filename=v.filename,
                    blob=v.stream.read(),
                    filetype=v.content_type,
                    size=v.content_length,
                    mimetype=v.mimetype,
                    mimetype_params=v.mimetype_params,
                )
                to_add.append(file_model)
                newAdmissao.files.append(file_model)

            newAdmissao.form_registry = registryAdmissional
            to_add.append(newAdmissao)
            db.session.add_all(to_add)
            db.session.commit()

        return await make_response(jsonify(ok="ok"))
