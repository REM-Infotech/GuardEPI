from .auth import LoginForm
from .recovery import ForgotPassword, ByPassRecover
from .globals import IMPORTEPIForm
from .groups import CreateGroup, SetPermsGroups, AddUsersGroup
from .create import (
    CadastroCargo,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroEPIForm,
    CadastroFuncionario,
    CadastroGrade,
)
from .edit import (
    EditCargo,
    EditDepartamentos,
    EditEmpresa,
    EditFuncionario,
    EditItemProdutoForm,
    EditSaldoGrade,
    ChangeEmail,
    ChangePassWord,
    AdmChangeEmail,
    AdmChangePassWord,
)

__all__ = [
    CadastroCargo,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroEPIForm,
    CadastroFuncionario,
    CadastroGrade,
    EditCargo,
    EditDepartamentos,
    EditEmpresa,
    EditFuncionario,
    EditItemProdutoForm,
    EditSaldoGrade,
    ChangeEmail,
    ChangePassWord,
    AdmChangeEmail,
    AdmChangePassWord,
    CreateGroup,
    SetPermsGroups,
    AddUsersGroup,
    IMPORTEPIForm,
    ForgotPassword,
    ByPassRecover,
    LoginForm,
]
