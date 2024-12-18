from importlib import import_module
from pathlib import Path

from flask import Blueprint, redirect, url_for

template_folder = Path(__file__).parent.resolve().joinpath("templates")
epi = Blueprint("epi", __name__, template_folder=template_folder, url_prefix="/epi")


@epi.get("/")
def redirecting():

    return redirect(url_for("epi.Equipamentos"))


if epi is not None:

    def epi_bp():

        import_module(".categorias", package=__package__)
        import_module(".cautelas", package=__package__)
        import_module(".equipamentos", package=__package__)
        import_module(".estoque", package=__package__)
        import_module(".fornecedores", package=__package__)
        import_module(".grade", package=__package__)
        import_module(".marcas", package=__package__)
        import_module(".modelos", package=__package__)

    epi_bp()
