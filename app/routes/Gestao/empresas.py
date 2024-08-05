from flask import *
from flask_login import *
from app import app
from app import db
from app.Forms import *
from app.models import *
from app.misc import *
from app.routes.CRUD.create import *
from app.routes.CRUD.update import *
from app.routes.CRUD.delete import *
from app.routes.EPI.cautela import *
from app.decorators import read_perm, set_endpoint

def set_choices() -> list[tuple[str, str]]:

    dbase = ProdutoEPI.query.all()

    return [(epi.nome_epi, epi.nome_epi) for epi in dbase]


@app.route("/Empresas", methods=["GET", "POST"])
@login_required
@set_endpoint
@read_perm
def Empresas():

    importForm = IMPORTEPIForm()
    form = CadastroEmpresa()
    database = Empresa.query.all()
    import_endpoint = 'importacao_corporativo'
    if request.method == "POST" and form.validate_on_submit():
        file = form.imagem.data
        docname = secure_filename(file.filename)
        now = generate_pid()
        filename = f"{now}.png"
        path_img = os.path.join(
            app.config['Temp_Path'], filename)
        file.save(path_img)

        with open(path_img, 'rb') as fileimg:
            binaryimage = fileimg.read()

        check_cadastro = Empresa.query.filter(
            Empresa.cnpj_empresa == form.cnpj.data).first()
        location = url_for(request.endpoint)
        if check_cadastro:
            flash("Empresa ja cadastrada!", "error")
            return redirect(location)

        CadEmpresa = Empresa(
            nome_empresa=form.empresa.data,
            cnpj_empresa=form.cnpj.data,
            imagem=filename,
            blob_imagem=binaryimage
        )

        db.session.add(CadEmpresa)
        db.session.commit()

        flash("Empresa cadastrada com sucesso!", "success")
        return redirect(location)

    DataTables = f'js/{request.endpoint.capitalize()}Table.js'
    page = f"pages/{request.endpoint.lower()}.html"
    return render_template("index.html", page=page, form=form, DataTables=DataTables,
                           database=database, import_endpoint=import_endpoint, 
                           importForm=importForm)
