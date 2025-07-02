from quart import Quart  # noqa: D104
from quart_socketio import SocketIO

from dusdoc_api.app.domain.admin import registry_admin
from dusdoc_api.app.domain.funcionarios import registry_funcionarios


async def register_quart(app: Quart, io: SocketIO) -> None:  # noqa: D103
    await registry_admin(app, io)
    await registry_funcionarios(app, io)
