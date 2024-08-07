from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     PasswordField, BooleanField, SelectMultipleField)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length

endpoints = [
    ("registros", "registros"),
    ("users", "users"),
    ("groups", "groups"),
    ("Equipamentos", "Equipamentos"),
    ("Estoque", "Estoque"),
    ("Estoque_Grade", "Estoque_Grade"),
    ("Entradas", "Entradas")
    ("Cautelas", "Cautelas")
    ("Grade", "Grade")
    ("cargos", "cargos")
    ("Empresas", "Empresas")
    ("funcionarios", "funcionarios")
    ("Departamentos", "Departamentos")
]


class CreateUserForm(FlaskForm):

    nome = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Senha", validators=[
                             DataRequired(), Length(min=8, max=62)])
    show_password = BooleanField('Exibir senha', id='check')
    submit = SubmitField(label="Criar")


class CreateGroup(FlaskForm):

    nome = StringField(label="Nome do Grupo", validators=[DataRequired()])
    paginas = SelectField(label="Selecione a página", validators=[
                          DataRequired()], choices=endpoints)

    permisions = SelectMultipleField("Selecione as permissões", choices=[
        ("CREATE", "Criar"),
        ("READ", "Visualizar",),
        ("UPDATE", "Editar"),
        ("DELETE", "Deletar")])
