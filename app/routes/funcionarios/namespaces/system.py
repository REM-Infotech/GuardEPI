from quart_socketio import Namespace  # noqa: D100

session = set()


class DusdocNamespace(Namespace):  # noqa: D101
    async def on_connect(self) -> None:
        """"""  # noqa: D419

    async def on_get_status_system(self) -> bool:
        """Handle a request for the status of the server."""
        # If the token is valid, proceed with the request
        return True

    async def on_test(self) -> dict[str, str]:
        return {"test": "test"}
