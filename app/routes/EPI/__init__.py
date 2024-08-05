from flask import *
from flask_login import *
from app import app
from app.Forms import *
from app.models import *
from app.misc import *
from app.routes.CRUD.create import *
from app.routes.CRUD.update import *
from app.routes.CRUD.delete import *
from app.routes.EPI.emitir_cautela import *


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





@app.route("/Cautelas")
@login_required
def Cautelas():

    page = "pages/Cautelas.html"
    database = RegistrosEPI.query.all()
    title = request.endpoint.capitalize()
    DataTables = 'js/CautelasTable.js'
    form = Cautela()
    session["itens_lista_cautela"] = []
    dbase_produto = ProdutoEPI.query.all()
    dbase_funcionario = Funcionarios.query.all()
    form.nome_epi.choices.extend([(epi.nome_epi, epi.nome_epi) for epi in dbase_produto])
    form.select_funcionario.choices.extend([(epi.nome_funcionario, epi.nome_funcionario) for epi in dbase_funcionario])
    return render_template("index.html", page=page, title=title, database=database, DataTables=DataTables, form=form)
