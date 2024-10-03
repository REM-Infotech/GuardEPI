from app.Forms.auth import LoginForm
from app.Forms.create.epi import (
    CadastroClasses, CadastroEPIForm,CadastroFonecedores, 
    CadastroGrade, CadastroMarcas, CadastroModelos, 
    Cautela, InsertEstoqueForm)

from app.Forms.create.gestao import CadastroCargo, CadastroDepartamentos, CadastroEmpresa, CadastroFuncionario
from app.Forms.create.user import CreateUserForm, CreatePerm, CreateGroup
from app.Forms.edit import (EditCargo, EditDepartamentos, EditFuncionario,
                            EditEmpresa, EditFuncionario, EditItemProdutoForm,
                            EditSaldoGrade, ChangeEmail, ProfileEditForm, AdmChangeEmail, 
                            AdmChangePassWord, ChangePassWord)
from app.Forms.recovery import ForgotPassword, ByPassRecover
from app.Forms.globals import IMPORTEPIForm
from app.Forms.groups import CreateGroup

