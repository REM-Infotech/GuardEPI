from flask_wtf import FlaskForm
from wtforms import (StringField, SelectField, SubmitField, DateField, FileField,
                     EmailField, TextAreaField)
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField

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