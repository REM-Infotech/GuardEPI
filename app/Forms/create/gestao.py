from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, TextAreaField, SelectField, EmailField, DateField)

from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length

from app import app

from app.models import Empresa, Departamento, Cargos

permited_file = FileAllowed(['png', 'jpg', 
                             'jpeg'], 'Apenas arquivos de imagem são permitidos!')

def setChoices_Empresa() -> list[tuple[str, str]]:
    
    with app.app_context():
        return [(query.nome_empresa, query.nome_empresa) for query in Empresa.query.all()]
    
def setChoices_Departamento() -> list[tuple[str, str]]:    

    with app.app_context():
        return [(query.departamento, query.departamento) for query in Departamento.query.all()]

def setChoices_Cargo() -> list[tuple[str, str]]:  

    with app.app_context():
        return [(query.cargo, query.cargo) for query in Cargos.query.all()]

class CadastroFuncionario(FlaskForm):

    codigo = StringField("Código de Identificação",
                         validators=[DataRequired(), Length(max=6)])
    nome_funcionario = StringField("Nome do funcionário", validators=[
                                   DataRequired("Informe o nome!")])
    cpf_funcionario = StringField("CPF do Funcionário", validators=[
                                  Length(min=11, max=14), DataRequired("Informe o CPF!")])
    email_funcionario = EmailField("Email")
    deficiencia = StringField("Deficiência")
    data_admissao = DateField("Data Admissão")
    empresa = SelectField("Empresa", validators=[
                          DataRequired("Informe uma empresa!")], choices=setChoices_Empresa())
    cargo = SelectField("Cargo", validators=[
                        DataRequired("Informe um Cargo!")], choices=setChoices_Cargo())
    departamento = SelectField("Departamento", validators=[
                               DataRequired()], choices=setChoices_Departamento())
    submit = SubmitField("Salvar alterações")

    def __init__(self, *args, **kwargs):
        super(CadastroFuncionario, self).__init__(*args, **kwargs)
        
        self.empresa.choices.extend(setChoices_Empresa())
        self.departamento.choices.extend(setChoices_Departamento())
        self.cargo.choices.extend(setChoices_Cargo())
        
class CadastroEmpresa(FlaskForm):

    nome_empresa = StringField("Nome da Empresa", validators=[DataRequired()])
    cnpj_empresa = StringField("CNPJ empresa", validators=[
                       Length(min=14, max=18), DataRequired()])
    filename = FileField("LOGO Da Empresa", validators=[FileRequired()])
    submit = SubmitField("Cadastrar!")


class CadastroCargo(FlaskForm):

    cargo = StringField("Nome do Cargo", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar!")


class CadastroDepartamentos(FlaskForm):

    departamento = StringField(
        "Nome do departamento", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar!")