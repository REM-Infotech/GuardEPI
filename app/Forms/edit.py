from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, SubmitField, IntegerField, DateField, FileField,
                     EmailField, TextAreaField)
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField, FileAllowed

from datetime import datetime
import pytz
class EditSaldoGrade(FlaskForm):

    nome_epi = StringField(label='Nome EPI')
    tipo_grade = StringField(label='Grade')
    qtd_estoque = IntegerField(label='Quantidade Estoque')
    tipo_qtd = StringField(label='Tipo do EPI')
    submit = SubmitField(label='Salvar')


class EditItemProdutoForm(FlaskForm):

    ca = StringField(label='CA')
    cod_ca = IntegerField(label='Cod CA')
    nome_epi = StringField(label='Nome do EPI')
    tipo_epi = StringField(label='Tipo do EPI')
    valor_unitario = StringField(label='Valor Unitário')
    qtd_entregar = IntegerField(label='Quantidade a Entregar')
    periodicidade_item = IntegerField(label='Periodicidade do Item')
    data_ultima_troca = DateField(label='Data da Última Troca')
    data_proxima_troca = DateField(label='Data da Próxima Troca')
    fornecedor = StringField(label='Fornecedor')
    marca = StringField(label='Marca')
    modelo = StringField(label='Modelo')
    imagem = FileField(label='Foto do EPI', id="imagem", validators=[
                       FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Salvar')

class EditFuncionario(FlaskForm):

    codigo = StringField("Código de Identificação", validators=[DataRequired()])
    nome_funcionario = StringField("Nome do funcionário", validators=[DataRequired("Informe o nome!")])
    cpf_funcionario = StringField("CPF do Funcionário", validators=[Length(min=11, max=14), DataRequired("Informe o CPF!")])
    email_funcionario = EmailField("Email")
    deficiencia = StringField("Deficiência")
    data_admissao = DateField("Data Admissão", format='%d-%m-%Y')
    empresa = SelectField("Empresa", validators=[DataRequired("Informe uma empresa!")], choices=[])
    cargo = SelectField("Cargo", validators=[DataRequired("Informe um Cargo!")], choices=[])
    departamento = SelectField("Departamento", validators=[DataRequired()], choices=[])
    submit = SubmitField("Salvar alterações")
    
class EditEmpresa(FlaskForm):
    
    nome_empresa = StringField("Nome da Empresa",validators=[DataRequired()])
    cnpj_empresa = StringField("CNPJ empresa", validators=[Length(min=14, max=18), DataRequired()])
    imagem = FileField("LOGO Da Empresa")
    submit = SubmitField("Salvar alterações")
    
class EditCargo(FlaskForm):

    cargo = StringField("Nome do Cargo",validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar alterações")

class EditDepartamentos(FlaskForm):

    departamento = StringField("Nome do departamento", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar alterações")