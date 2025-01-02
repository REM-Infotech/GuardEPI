from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

from .auth import LoginForm
from .create.epi import (
    CadastroCategorias,
    CadastroEPIForm,
    CadastroFornecedores,
    CadastroGrade,
    CadastroMarcas,
    CadastroModelos,
    Cautela,
    InsertEstoqueForm,
)
from .create.gestao import (
    CadastroCargo,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroFuncionario,
)
from .create.user import CreateGroup, CreatePerm, CreateUserForm
from .edit import (
    AdmChangeEmail,
    AdmChangePassWord,
    ChangeEmail,
    ChangePassWord,
    EditCargo,
    EditDepartamentos,
    EditEmpresa,
    EditFuncionario,
    EditItemProdutoForm,
    EditSaldoGrade,
    ProfileEditForm,
)
from .recovery import ByPassRecover, ForgotPassword
from .schedule_task import TaskNotificacaoForm

__all__ = [
    LoginForm,
    CadastroCargo,
    CadastroCategorias,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroDepartamentos,
    CadastroEPIForm,
    CadastroFornecedores,
    CadastroFuncionario,
    CadastroGrade,
    CadastroMarcas,
    CadastroModelos,
    Cautela,
    InsertEstoqueForm,
    EditCargo,
    CreateUserForm,
    CreatePerm,
    CreateGroup,
    ForgotPassword,
    ByPassRecover,
    EditDepartamentos,
    EditFuncionario,
    EditEmpresa,
    EditFuncionario,
    EditItemProdutoForm,
    EditSaldoGrade,
    ChangeEmail,
    ProfileEditForm,
    AdmChangeEmail,
    AdmChangePassWord,
    ChangePassWord,
    TaskNotificacaoForm,
]


permited_file = FileAllowed(["xlsx", "xls"], 'Apenas arquivos ".xlsx" são permitidos!')


class ImporteLotesForm(FlaskForm):
    arquivo = FileField(
        label="Arquivo de importação. Máximo 50Mb",
        validators=[FileRequired(), permited_file],
    )
    submit = SubmitField(label="Importar")
