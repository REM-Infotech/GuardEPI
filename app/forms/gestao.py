from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    DateField,
    EmailField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length

from app.models import Cargos, Departamento, Empresa

permited_file = FileAllowed(
    ["png", "jpg", "jpeg"], "Apenas arquivos de imagem são permitidos!"
)


def setChoices_Empresa() -> list[tuple[str, str]]:
    return [(query.nome_empresa, query.nome_empresa) for query in Empresa.query.all()]


def setChoices_Departamento() -> list[tuple[str, str]]:
    return [
        (query.departamento, query.departamento) for query in Departamento.query.all()
    ]


def setChoices_Cargo() -> list[tuple[str, str]]:
    return [(query.cargo, query.cargo) for query in Cargos.query.all()]


class FuncionarioForm(FlaskForm):
    codigo = StringField(
        "Código de Identificação",
        validators=[DataRequired(), Length(max=6)],
        default="000001",
    )
    nome = StringField(
        "Nome do funcionário", validators=[DataRequired("Informe o nome!")]
    )
    cpf = StringField(
        "CPF do Funcionário",
        validators=[Length(min=11, max=14), DataRequired("Informe o CPF!")],
    )
    email = EmailField("Email")
    deficiencia = StringField("Deficiência", default="Não Consta")
    data_admissao = DateField("Data Admissão", default=datetime.now())
    empresa = SelectField(
        "Empresa",
        validators=[DataRequired("Informe uma empresa!")],
        choices=[],
    )
    cargo = SelectField(
        "Cargo",
        validators=[DataRequired("Informe um Cargo!")],
        choices=[],
    )
    departamento = SelectField("Departamento", validators=[DataRequired()], choices=[])
    submit = SubmitField("Salvar alterações")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.empresa.choices.extend(setChoices_Empresa())
        self.departamento.choices.extend(setChoices_Departamento())
        self.cargo.choices.extend(setChoices_Cargo())


class EmpresaForm(FlaskForm):
    nome_empresa = StringField("Nome da Empresa", validators=[DataRequired()])
    cnpj_empresa = StringField(
        "CNPJ empresa", validators=[Length(min=14, max=18), DataRequired()]
    )
    filename = FileField("LOGO Da Empresa", validators=[FileRequired()])
    submit = SubmitField("Salvar")


class CargoForm(FlaskForm):
    cargo = StringField("Nome do Cargo", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Salvar")


class FormDepartamentos(FlaskForm):
    departamento = StringField("Nome do departamento", validators=[DataRequired()])
    descricao = TextAreaField("Descrição (Opcional)", default="Sem descrição")
    submit = SubmitField("Salvar")
