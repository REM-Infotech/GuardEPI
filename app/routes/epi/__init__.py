from importlib import import_module
from pathlib import Path

from flask import Blueprint, redirect, url_for
from werkzeug.wrappers.response import Response

template_folder = Path(__file__).parent.resolve().joinpath("templates")
epi = Blueprint("epi", __name__, template_folder=template_folder, url_prefix="/epi")
estoque_bp = Blueprint(
    "estoque", __name__, template_folder=template_folder, url_prefix="/estoque"
)


@epi.get("/")
def redirecting() -> Response:
    """
    Redirects to the 'Equipamentos' endpoint within the 'epi' blueprint.
    Returns:
        Response: A redirect response object to the 'epi.Equipamentos' URL.
    """

    return redirect(url_for("epi.Equipamentos"))


if epi is not None:

    def epi_bp() -> None:
        """
        Import various modules related to 'epi' (personal protective equipment).
        This function imports the following modules:
        - .categorias: Handles categories of equipment.
        - .cautelas: Manages cautions or warnings.
        - .equipamentos: Manages equipment details.
        - .estoque: Manages inventory or stock.
        - .fornecedores: Manages suppliers.
        - .grade: Handles grading or classification.
        - .marcas: Manages brands.
        - .modelos: Manages models.
        Each module is imported using the import_module function from the importlib package.
        """

        import_module(".categorias", package=__package__)
        import_module(".cautelas", package=__package__)
        import_module(".equipamentos", package=__package__)
        import_module(".estoque", package=__package__)
        import_module(".fornecedores", package=__package__)
        import_module(".grade", package=__package__)
        import_module(".marcas", package=__package__)
        import_module(".modelos", package=__package__)

    epi_bp()
