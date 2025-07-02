# noqa: D104


from quart import Quart
from quart_socketio import SocketIO

from .namespaces.docs import FuncionarioDocsNamespace
from .namespaces.forms import FuncionarioFormsNamespace
from .namespaces.system import DusdocNamespace


async def register_routes_funcionarios(app: Quart) -> None:
    """Register all routes with the Quart application."""
    from .routes.auth import auth
    from .routes.forms import forms

    blueprints = [auth, forms]

    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    # Add any additional routes or blueprints here as needed


async def register_api_funcionario(app: Quart) -> None:  # noqa: D103
    from app.models.Funcionários import Funcionarios as Users

    from .routes.forms import forms
    from .routes.forms.admissional import AdmissionalFormView

    form_admissional = AdmissionalFormView.as_view("AdmissionalForm", Users)
    forms.add_url_rule("/admissional/<int:_id>", view_func=form_admissional)


async def register_namespace_funcionario(io: SocketIO) -> None:  # noqa: D103
    namespaces = [
        DusdocNamespace("/", io),
        FuncionarioFormsNamespace("/funcionario_forms", io),
        FuncionarioDocsNamespace("/funcionario_informacoes", io),
    ]

    for namespace in namespaces:
        await io.register_namespace(namespace)


async def registry_funcionarios(app: Quart, io: SocketIO) -> None:  # noqa: D103
    await register_api_funcionario(app)
    await register_routes_funcionarios(app)
    await register_namespace_funcionario(io)
