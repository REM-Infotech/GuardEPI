from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, PasswordField,
                     DateField, IntegerField, BooleanField, EmailField, TextAreaField, SelectMultipleField)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length


permited_file = FileAllowed(
    ['xlsx', 'xls'], 'Apenas arquivos ".xlsx" são permitidos!')


class CadastroGradeForm(FlaskForm):

    nome_epi = SelectField(label='EPI', choices=[("Vazio", "Selecione")], validators=[DataRequired()])
    tipo_grade = StringField(label='Grade', validators=[DataRequired()])
    tipo_qtd = StringField(
        label='Tipo de Quantidade(Ex.: Peça, Unidade, Par, etc)', validators=[DataRequired()])
    qtd_estoque = IntegerField(label='Quantidade em Estoque', validators=[DataRequired()])
    submit = SubmitField(label='Salvar')


permited_file = FileAllowed(
    ['xlsx', 'xls'], 'Apenas arquivos ".xlsx" são permitidos!')


class CadastroEPIForm(FlaskForm):

    ca = StringField(label='CA', validators=[DataRequired()])
    cod_ca = IntegerField(label='Cod CA', validators=[DataRequired()])
    nome_epi = StringField(label='Nome do EPI', validators=[DataRequired()])
    tipo_epi = StringField(label='Tipo do EPI', validators=[DataRequired()])
    valor_unitario = StringField(label='Valor Unitário', validators=[DataRequired()])
    qtd_entregar = IntegerField(label='Quantidade a Entregar')
    periodicidade_item = IntegerField(label='Periodicidade do Item')
    vencimento = DateField(label='Vencimento', format='%d-%m-%Y')
    fornecedor = StringField(label='Fornecedor')
    marca = StringField(label='Marca')
    modelo = StringField(label='Modelo')
    imagem = FileField(label='Foto do EPI', id="imagem", validators=[
                       FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField(label='Salvar')


class CadastroCautela(FlaskForm):

    select_funcionario = SelectField(label="Selecione o Funcionário", validators=[
                                     DataRequired()], choices=[])
    nome_epi = SelectField(id="selectNomeEpi", label="Selecione a EPI", choices=[
                           ("Vazio", "Selecione")])
    tipo_grade = StringField(label='Informe a grade')
    qtd_entregar = IntegerField(
        label="Quantidade para entregar", validators=[Length(min=1)])
    submit_cautela = SubmitField(
        id="submit_cautela", label="Emitir documento", render_kw={'type': 'button'})


class CreateUserForm(FlaskForm):

    nome = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Senha", validators=[DataRequired(), Length(min=8, max=62)])
    show_password = BooleanField('Exibir senha', id='check')
    submit = SubmitField(label="Criar")


class Cautela(FlaskForm):

    select_funcionario = SelectField(label="Selecione o Funcionário", validators=[
                                     DataRequired()], choices=[("Vazio", "Selecione")])
    nome_epi = SelectField(id="selectNomeEpi", label="Selecione a EPI", choices=[
                           ("Vazio", "Selecione")])
    tipo_grade = SelectField(id="selectNomeEpi", label="Selecione a Grade", choices=[])
    qtd_entregar = IntegerField(
        label="Quantidade para entregar", validators=[Length(min=1)])
    submit_cautela = SubmitField(id="submit_cautela", label="Emitir documento")


class CadastroFuncionario(FlaskForm):

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

class CadastroEmpresa(FlaskForm):
    
    empresa = StringField("Nome da Empresa",validators=[DataRequired()])
    cnpj = StringField("CNPJ empresa", validators=[Length(min=14, max=18), DataRequired()])
    imagem = FileField("LOGO Da Empresa")
    submit = SubmitField("Cadastrar!")
    
class CadastroCargo(FlaskForm):

    cargo = StringField("Nome do Cargo",validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar!")

class CadastroDepartamentos(FlaskForm):

    departamento = StringField("Nome do departamento", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Cadastrar!")
