import asyncio
import secrets
from contextlib import suppress
from os import environ

import uvicorn

from app import create_app


async def main() -> None:
    """Run socketio server."""

    def get_random_port() -> int:
        return secrets.randbelow(65535 - 1024) + 1024

    port = int(environ.get("PORT", get_random_port()))

    app = await create_app()
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")  # noqa: S104
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
