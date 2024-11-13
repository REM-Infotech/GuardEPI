from .auth import LoginForm
from .globals import IMPORTEPIForm
from .recovery import ForgotPassword, ByPassRecover
from .create.user import CreateUserForm, CreatePerm, CreateGroup
from .create.epi import (
    CadastroClasses,
    CadastroEPIForm,
    CadastroFonecedores,
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

from .edit import (
    EditCargo,
    EditDepartamentos,
    EditFuncionario,
    EditEmpresa,
    EditItemProdutoForm,
    EditSaldoGrade,
    ChangeEmail,
    ProfileEditForm,
    AdmChangeEmail,
    AdmChangePassWord,
    ChangePassWord,
)


__all__ = [
    LoginForm,
    CadastroCargo,
    CadastroClasses,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroDepartamentos,
    CadastroEPIForm,
    CadastroFonecedores,
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
    IMPORTEPIForm,
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
]
