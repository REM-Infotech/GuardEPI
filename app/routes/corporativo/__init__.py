from pathlib import Path

from flask import Blueprint

from . import cargos, departamentos, empresas, funcionarios

template_folder = Path(__file__).parent.resolve().joinpath("templates")
corp = Blueprint(
    "corp", __name__, template_folder=template_folder, prefix="/corporativo"
)


__all__ = [cargos, empresas, funcionarios, departamentos]
