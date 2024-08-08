from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField,
                     PasswordField, BooleanField, SelectMultipleField, TextAreaField)
from wtforms.validators import DataRequired, Length
from app.models import Users

endpoints = [
    ("registros", "Registros"),
    ("users", "Usuários"),
    ("groups", "Grupos"),
    ("Equipamentos", "Equipamentos"),
    ("Estoque", "Estoque"),
    ("Estoque_Grade", "Estoque de grades"),
    ("Entradas", "Entradas"),
    ("Cautelas", "Cautelas"),
    ("Grade", "Grade"),
    ("cargos", "Cargos"),
    ("Empresas", "Empresas"),
    ("funcionarios", "Funcionários"),
    ("Departamentos", "Departamentos")
]


def set_choicesUsers() -> list[tuple[str, str]]:

    return [(item.login, item.nome_usuario) for item in Users.query.all()]


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
    desc = TextAreaField("Descrição (Opcional)")
    
    def __init__(self, *args, **kwargs):
        super(CreateGroup, self).__init__(*args, **kwargs)
        
        self.users.choices.extend(set_choicesUsers())
