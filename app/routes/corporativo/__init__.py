import traceback
from importlib import import_module
from pathlib import Path

from quart import Blueprint, abort, make_response, redirect, url_for
from quart import current_app as app
from werkzeug import Response

template_folder = Path(__file__).parent.resolve().joinpath("templates")
corp = Blueprint(
    "corp", __name__, template_folder=template_folder, url_prefix="/corporativo"
)


@corp.get("/")
def redirecting() -> Response:
    try:
        return await make_response(redirect(url_for("corp.Empresas")))

    except Exception:
        app.logger.exception(traceback.format_exc())
        abort(500)


if corp is not None:

    def corp_bp() -> None:
        """
        Initialize the corporate blueprint by importing necessary modules.

        This function imports the following modules:
        - .cargos: Handles operations related to job positions.
        - .departamentos: Manages department-related functionalities.
        - .empresas: Deals with company-related operations.
        - .funcionarios: Manages employee-related functionalities.

        Returns:
            None
        """
        import_module(".cargos", package=__package__)
        import_module(".departamentos", package=__package__)
        import_module(".empresas", package=__package__)
        import_module(".funcionarios", package=__package__)

    corp_bp()
