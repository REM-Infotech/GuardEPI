from flask import abort, render_template
from flask_login import login_required

from app.forms import CadastroFuncionario
from app.models.Funcionários import Funcionarios

from . import corp


@corp.get("/funcionarios")
@login_required
def funcionarios():
    """
    Fetches all records from the Funcionarios table and renders the 'index.html' template with the data.
    This function queries all records from the Funcionarios table in the database and passes the data to the
    'index.html' template along with the page name 'funcionarios.html'. If an exception occurs during the process,
    it aborts the request with a 500 status code and includes the exception message in the response.
    Returns:
        Response: A Flask response object that renders the 'index.html' template with the fetched data.
    Raises:
        HTTPException: If an exception occurs, it aborts the request with a 500 status code and the exception message.
    """

    try:

        page = "funcionarios.html"
        database = Funcionarios.query.all()
        return render_template(
            "index.html",
            page=page,
            database=database,
        )
    except Exception as e:
        abort(500, description=str(e))


@corp.route("/funcionarios/cadastro")
@login_required
def cadastro():

    form = CadastroFuncionario()

    if form.validate_on_submit():
        pass

    return render_template("index.html", form=form)
