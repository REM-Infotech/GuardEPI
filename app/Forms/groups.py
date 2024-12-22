from flask_wtf import FlaskForm  # pragma: no cover
from wtforms import SelectMultipleField, StringField, SubmitField  # pragma: no cover
from wtforms.validators import DataRequired  # pragma: no cover

from app.models import Groups, Users  # pragma: no cover

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
    ("cargo.cargos", "cargo.cargos"),
    ("Departamentos", "Departamentos"),
]  # pragma: no cover


def setRules() -> list[tuple[str, str]]:  # pragma: no cover
    return [
        ("CREATE", "Criar"),
        ("READ", "Acesso a informações"),
        ("UPDATE", "Alterar Dados"),
        ("DELETE", "Deletar Informações"),
    ]


def set_choicesUsers() -> list[tuple[str, str]]:  # pragma: no cover
    return [(item.login, item.nome_usuario) for item in Users.query.all()]


def set_choicesGroups() -> list[tuple[str, str]]:  # pragma: no cover
    return [(item.name_group, item.name_group) for item in Groups.query.all()]


class CreateGroup(FlaskForm):  # pragma: no cover
    nome = StringField(label="Nome do Grupo", validators=[DataRequired()])
    membros = SelectMultipleField(
        "Selecione os Integrantes", validators=[DataRequired()], choices=[]
    )
    submit = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.membros.choices.extend(set_choicesUsers())
