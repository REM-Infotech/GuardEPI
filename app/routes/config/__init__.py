from importlib import import_module
from pathlib import Path

from flask import Blueprint, redirect, url_for

template_folder = Path(__file__).parent.resolve().joinpath("templates")
config = Blueprint(
    "config", __name__, template_folder=template_folder, url_prefix="/config"
)


@config.get("/")
def redirecting():
    """
    Redirects to the 'Equipamentos' endpoint within the 'epi' blueprint.
    Returns:
        Response: A redirect response object to the 'epi.Equipamentos' URL.
    """

    return redirect(url_for("epi.Equipamentos"))


import_module(".users", __package__)
import_module(".groups", __package__)
import_module(".roles", __package__)
