from flask import render_template, request
from flask_login import login_required
from app import app
from app.Forms.create import CadastroEPIForm
from app.Forms.globals import IMPORTEPIForm
from app.models.EPI import ProdutoEPI
from app.misc import format_currency_brl


@app.route("/Equipamentos")
@login_required
def Equipamentos():

    importForm = IMPORTEPIForm()
    form = CadastroEPIForm()
    page = "pages/Equipamentos.html"
    title = request.endpoint.capitalize()
    database = ProdutoEPI.query.all()
    DataTables = 'js/EquipamentosTable.js'
    url = "https://cdn-icons-png.flaticon.com/512/11547/11547438.png"
    return render_template("index.html", page=page, title=title, form=form,
                           importForm=importForm, database=database,
                           format_currency_brl=format_currency_brl,
                           DataTables=DataTables, url_image=url)


