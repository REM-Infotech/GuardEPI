from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (StringField, SubmitField, SelectField,
                     PasswordField, BooleanField, SelectMultipleField, TextAreaField)
from wtforms.validators import DataRequired, Length
from app.models import Users

endpoints = [
    ("Equipamentos", "Equipamentos"),
    ("Grade", "Grades"),
    ("Fornecedores", "Fornecedores"),
    ("Marcas", "Marcas"),
    ("Modelos", "Modelos"),
    ("Classes", "Classes"),
    ("Estoque", "Estoque Geral"),
    ("Estoque_Grade", "Estoque por Grade"),
    ("Entradas", "Registro Entradas"),
    ("Registro_Saidas", "Registro Saídas"),
    ("Cautelas", "Cautelas"),
    ("funcionarios", "funcionarios"),
    ("Empresas", "Empresas"),
    ("cargos", "cargos"),
    ("Departamentos", "Departamentos"),
    ("users", "users"),
    ("groups", "groups"),
    ("Permissoes", "Permissoes")
]

perms = [("CREATE", "Criar e Adicionar Itens"),
         ("READ", "Acessar Informações"),
         ("UPDATE", "Atualizar Informações"),
         ("DELETE", "Deletar Informações")]


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

class CreatePerm(FlaskForm):
    
    name_rule = StringField(label="Nome do Grupo", validators=[DataRequired()])
    grupos = SelectMultipleField("Selecione os Grupos", choices=[])
    rota = SelectField("Selecione a Página", choices=endpoints)
    permissoes = SelectMultipleField("Selecione as Permissões", choices=perms)
    submit = SubmitField("Salvar Alterações")
    
    def __init__(self, *args, **kwargs):
        super(CreatePerm, self).__init__(*args, **kwargs)
    
    