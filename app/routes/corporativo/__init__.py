from importlib import import_module
from pathlib import Path

from flask import Blueprint, redirect, url_for
from werkzeug import Response

template_folder = Path(__file__).parent.resolve().joinpath("templates")
corp = Blueprint(
    "corp", __name__, template_folder=template_folder, url_prefix="/corporativo"
)


@corp.get("/")
def redirecting() -> Response:

    return redirect(url_for("corp.Empresas"))


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
