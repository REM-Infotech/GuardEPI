from flask import abort, render_template
from flask_login import login_required

from app.forms.create import CadastroEmpresa
from app.models.Funcionários import Empresa

from . import corp


@corp.route("/Empresas", methods=["GET"])
@login_required
def Empresas():
    """
    Handles the route for displaying the 'Empresas' page.
    This function creates an instance of the CadastroEmpresa form and retrieves all records from the Empresa database.
    It then renders the 'index.html' template with the 'empresas.html' page, the form, and the database records.
    Returns:
        Response: The rendered template for the 'Empresas' page.
    Raises:
        HTTPException: If an error occurs during the process, a 500 Internal Server Error is raised with the error description.
    """

    try:

        form = CadastroEmpresa()
        database = Empresa.query.all()

        page = "empresas.html"
        return render_template(
            "index.html",
            page=page,
            form=form,
            database=database,
        )

    except Exception as e:
        abort(500, description=str(e))
