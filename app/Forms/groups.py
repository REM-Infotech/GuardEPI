from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import (StringField, SubmitField, SelectField,
                     PasswordField, BooleanField, SelectMultipleField, TextAreaField)
from wtforms.validators import DataRequired, Length
from app.models import Users, Groups

endpoints = [
    ("registros", "Registros"),
    ("users", "Usuários"),
    ("groups", "Grupos"),
    ("set1", "Produtos", False, {"disabled": True}),
    ("Equipamentos", "Info. Equipamentos"),
    ("Grade", "Info. Grade"),
    ("set2", "Estoque", False, {"disabled": True}),
    ("Estoque", "Equipamentos"),
    ("Estoque_Grade", "Grades"),
    ("Entradas", "Entradas"),
    ("Cautelas", "Cautelas"),
    ("funcionarios", "Funcionários"),
    ("Empresas", "Empresas"),
    ("cargos", "Cargos"),
    ("Departamentos", "Departamentos")
]

def setRules() -> list[tuple[str, str]]:
    
    return [
        ("CREATE", "Criar"),
        ("READ", "Acesso a informações"),
        ("UPDATE", "Alterar Dados"),
        ("DELETE", "Deletar Informações")
        ]

def set_choicesUsers() -> list[tuple[str, str]]:

    return [(item.login, item.nome_usuario) for item in Users.query.all()]

def set_choicesGroups() -> list[tuple[str, str]]:

    return [(item.name_group, item.name_group) for item in Groups.query.all()]

class CreateGroup(FlaskForm):

    nome = StringField(label="Nome do Grupo", validators=[DataRequired()])
    membros = SelectMultipleField("Selecione os Integrantes", validators=[DataRequired()], choices = [])
    submit = SubmitField("Salvar Alterações")
    
    def __init__(self, *args, **kwargs):
        super(CreateGroup, self).__init__(*args, **kwargs)
        
        self.membros.choices.extend(set_choicesUsers())

