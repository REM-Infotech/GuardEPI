import asyncio
import secrets
from contextlib import suppress
from os import environ
from pathlib import Path

import uvicorn

from app import create_app


async def main() -> None:
    """Run socketio server."""

    def get_random_port() -> int:
        return secrets.randbelow(65535 - 1024) + 1024

    port = int(environ.get("PORT", get_random_port()))

    app = await create_app()
    app.debug = True
    config = uvicorn.Config(
        app,
        host="0.0.0.0",  # noqa: S104
        port=port,
        log_level="info",
        reload=True,
        reload_dirs=[Path(__file__).parent.resolve()],
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
