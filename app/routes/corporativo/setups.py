from pathlib import Path
from typing import Any

from quart import current_app as app
from quart import url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models import Funcionarios


async def setup_form_funcionario(funcionario: Funcionarios) -> tuple[dict, Any | str]:
    form_data = {}
    emp_data = {
        k: v
        for k, v in list(funcionario.__dict__.items())
        if v and (not k.startswith("_") or k != "id")
    }

    items_emp_data = list(
        {k: v for k, v in list(emp_data.items()) if k != "filename"}.items()
    )

    for key, value in items_emp_data:
        if key == "blob_doc" and value:
            img_path = (
                Path(app.config.get("TEMP_PATH"))
                .joinpath("IMG")
                .joinpath(emp_data.get("filename"))
            )
            with img_path.open("wb") as file:
                file.write(value)
                form_data.update(
                    {
                        "filename": FileStorage(
                            filename=secure_filename(funcionario.filename),
                            stream=value,
                        )
                    }
                )

                url_image = url_for(
                    "serve.serve_img", filename=funcionario.filename, _external=True
                )

            continue

        form_data.update({key: value})

    return form_data, url_image
