from pathlib import Path  # noqa: D100

from quart import request
from quart.datastructures import FileStorage
from quart_socketio import Namespace


class FuncionarioFormsNamespace(Namespace):  # noqa: D101
    async def on_admissional_form(self) -> bool | None:  # noqa: D102
        try:
            data = request.socket_data
            for _k, v in list(data.items()):
                if not isinstance(v, FileStorage):
                    if v is not None and v != "":
                        print(v)

            return True

        except Exception as e:
            print(e)
            return False

    async def on_admissional_files(self) -> bool:
        try:
            data = request.socket_data
            for _k, v in list(data.items()):
                if isinstance(v, FileStorage):
                    print(v.stream.read())

                    parent = Path(__file__).cwd().joinpath("dusdoc_api", "examples")
                    v.save(parent.joinpath(v.filename))
            return True

        except Exception as e:
            print(e)
            return False

        return True
