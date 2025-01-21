from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import FileField, SubmitField

from .auth import LoginForm
from .config import (
    AdmChangeEmail,
    AdmChangePassWord,
    ChangeEmail,
    ChangePassWord,
    FormRoles,
    FormUser,
    GroupForm,
    ProfileEditForm,
)
from .epi import (
    Cautela,
    FormCategorias,
    FormGrade,
    FormMarcas,
    FormModelos,
    FormProduto,
    FornecedoresForm,
    InsertEstoqueForm,
)
from .gestao import CargoForm, EmpresaForm, FormDepartamentos, FuncionarioForm

__all__ = [
    AdmChangeEmail,
    AdmChangePassWord,
    ChangeEmail,
    ChangePassWord,
    FormRoles,
    FormUser,
    LoginForm,
    ProfileEditForm,
    FormCategorias,
    FormGrade,
    FormMarcas,
    FormModelos,
    FormProduto,
    InsertEstoqueForm,
    Cautela,
    GroupForm,
    FormDepartamentos,
    FuncionarioForm,
    CargoForm,
    EmpresaForm,
    FornecedoresForm,
]

permited_file = FileAllowed(["xlsx", "xls"], 'Apenas arquivos ".xlsx" são permitidos!')


class ImporteLotesForm(FlaskForm):
    arquivo = FileField(
        label="Arquivo de importação. Máximo 50Mb",
        validators=[FileRequired(), permited_file],
    )
    submit = SubmitField(label="Importar")
