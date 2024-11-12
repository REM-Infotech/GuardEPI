from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    SelectMultipleField,
    TextAreaField,
)
from wtforms.validators import DataRequired
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
    ("Departamentos", "Departamentos"),
]


def setRules() -> list[tuple[str, str]]:

    return [
        ("CREATE", "Criar"),
        ("READ", "Acesso a informações"),
        ("UPDATE", "Alterar Dados"),
        ("DELETE", "Deletar Informações"),
    ]


def set_choicesUsers() -> list[tuple[str, str]]:

    return [(item.login, item.nome_usuario) for item in Users.query.all()]


def set_choicesGroups() -> list[tuple[str, str]]:

    return [(item.name_group, item.name_group) for item in Groups.query.all()]


class CreateGroup(FlaskForm):

    nome = StringField(label="Nome do Grupo", validators=[DataRequired()])
    desc = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar Alterações")


class AddUsersGroup(FlaskForm):

    selectgrupo = SelectField(
        "Selecione o Grupo", validators=[DataRequired()], choices=[]
    )
    selectUsers = SelectMultipleField(
        "Selecione os Usuários", validators=[DataRequired()], choices=[]
    )
    submit = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super(AddUsersGroup, self).__init__(*args, **kwargs)

        self.selectgrupo.choices.extend(set_choicesGroups())
        self.selectUsers.choices.extend(set_choicesUsers())


class SetPermsGroups(FlaskForm):

    selectgrupo = SelectMultipleField(
        "Selecione os Grupos", validators=[DataRequired()], choices=[]
    )
    selectRules = SelectMultipleField(
        "Selecione as Permissões", validators=[DataRequired()], choices=[]
    )
    submit = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super(SetPermsGroups, self).__init__(*args, **kwargs)

        self.selectgrupo.choices.extend(set_choicesGroups())
        self.selectRules.choices.extend(setRules())
