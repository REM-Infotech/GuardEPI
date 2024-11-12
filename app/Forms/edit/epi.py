from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, FileField
from flask_wtf.file import FileAllowed


class EditSaldoGrade(FlaskForm):

    nome_epi = StringField(label="Nome EPI")
    tipo_grade = StringField(label="Grade")
    qtd_estoque = IntegerField(label="Quantidade Estoque")
    tipo_qtd = StringField(label="Tipo do EPI")
    submit = SubmitField(label="Salvar")


class EditItemProdutoForm(FlaskForm):

    ca = StringField(label="CA")
    cod_ca = IntegerField(label="Cod CA")
    nome_epi = StringField(label="Nome do EPI")
    tipo_epi = StringField(label="Tipo do EPI")
    valor_unitario = StringField(label="Valor Unitário")
    qtd_entregar = IntegerField(label="Quantidade a Entregar")
    periodicidade_item = IntegerField(label="Periodicidade do Item")
    vencimento = DateField(label="Vencimento")
    fornecedor = StringField(label="Fornecedor")
    marca = StringField(label="Marca")
    modelo = StringField(label="Modelo")
    imagem = FileField(
        label="Foto do EPI",
        id="imagem",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")],
    )
    submit = SubmitField(label="Salvar")
