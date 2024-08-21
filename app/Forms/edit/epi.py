from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, SelectField, FileField)
from flask_wtf.file import FileField, FileAllowed, DataRequired

from app.Forms.choices import (set_choicesClasseEPI, 
                               set_choicesFornecedor, set_choicesMarca, 
                               set_choicesModelo)

class EditSaldoGrade(FlaskForm):

    nome_epi = StringField(label='Nome EPI')
    tipo_grade = StringField(label='Grade')
    qtd_estoque = IntegerField(label='Quantidade Estoque')
    tipo_qtd = StringField(label='Tipo do EPI')
    submit = SubmitField(label='Salvar')

class EditItemProdutoForm(FlaskForm):

    ca = StringField(label='CA', validators=[DataRequired()])
    cod_ca = IntegerField(label='Cod CA', validators=[DataRequired()])
    nome_epi = StringField(label='EPI', validators=[DataRequired()])
    tipo_epi = SelectField(label='Tipo do EPI', validators=[DataRequired()], choices=[])
    valor_unitario = StringField(
        label='Valor Unitário', validators=[DataRequired()])
    qtd_entregar = IntegerField(label='Quantidade a Entregar')
    periodicidade_item = IntegerField(label='Periodicidade do Item')
    fornecedor = SelectField(label='Fornecedor', choices=[])
    marca = SelectField(label='Marca', choices=[])
    modelo = SelectField(label='Modelo', choices=[])
    filename = FileField(label='Foto do EPI', id="imagem", validators=[
                       FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Salvar')

    def __init__(self, *args, **kwargs):

        super(EditItemProdutoForm, self).__init__(*args, **kwargs)
        self.fornecedor.choices.extend(set_choicesFornecedor())
        self.marca.choices.extend(set_choicesMarca())
        self.modelo.choices.extend(set_choicesModelo())
        self.tipo_epi.choices.extend(set_choicesClasseEPI())


