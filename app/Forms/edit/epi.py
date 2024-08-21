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
    tipo_epi = SelectField(label='Tipo do EPI', choices=[])
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
        
        
        ## Eu deixei com underline pra nao conflitar com os declarados
        ## do formulário
        
        ## :D
        
        fornecedor_ = [kwargs.get('fornecedor_selected')]
        marca_ = [kwargs.get('marca_selected')]
        modelo_ = [kwargs.get('modelo_selected')]
        tipoepi_ = [kwargs.get('tipoepi_selected')]
        
        fornecedor_choices = set_choicesFornecedor()
        marca_choices = set_choicesMarca()
        modelo_choices = set_choicesModelo()
        tipo_epi_choices = set_choicesClasseEPI()
        
        fornecedor_choices.extend(fornecedor_)
        marca_choices.extend(marca_)
        modelo_choices.extend(modelo_)
        tipo_epi_choices.extend(tipoepi_)
        
        self.fornecedor.choices.extend(fornecedor_choices)
        self.marca.choices.extend(marca_choices)
        self.modelo.choices.extend(modelo_choices)
        self.tipo_epi.choices.extend(tipo_epi_choices)
        
        
        
        


