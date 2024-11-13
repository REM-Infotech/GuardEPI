from flask_wtf import FlaskForm
from app.Forms import (
    CadastroCargo,
    CadastroDepartamentos,
    InsertEstoqueForm,
    CadastroEmpresa,
    CadastroEPIForm,
    CadastroGrade,
    CadastroFuncionario,
    CadastroFonecedores,
    CadastroClasses,
    CadastroMarcas,
    CadastroModelos,
)

from app.models import (
    ProdutoEPI,
    RegistrosEPI,
    EstoqueEPI,
    EstoqueGrade,
    RegistroEntradas,
    GradeEPI,
    Empresa,
    Funcionarios,
    Departamento,
    Cargos,
    Groups,
    ClassesEPI,
    ModelosEPI,
    Marcas,
    Fornecedores,
    Users,
)

from app.Forms.edit import (
    EditItemProdutoForm,
    EditSaldoGrade,
    EditFuncionario,
    EditEmpresa,
    EditDepartamentos,
    EditCargo,
)
from app import db
from typing import Type

tipo = db.Model


def get_models(tipo: str) -> Type[tipo]:

    models = {
        "equipamentos": ProdutoEPI,
        "estoque": EstoqueEPI,
        "grade": GradeEPI,
        "empresas": Empresa,
        "funcionarios": Funcionarios,
        "departamentos": Departamento,
        "cargos": Cargos,
        "cautelas": RegistrosEPI,
        "entradas": RegistroEntradas,
        "estoque_grade": EstoqueGrade,
        "groups": Groups,
        "users": Users,
        "classes": ClassesEPI,
        "modelos": ModelosEPI,
        "marcas": Marcas,
        "fornecedores": Fornecedores,
    }

    return models[tipo]


def getformCad(form) -> Type[FlaskForm]:

    forms = {
        "equipamentos": CadastroEPIForm(),
        "empresas": CadastroEmpresa(),
        "estoque": InsertEstoqueForm(),
        "departamentos": CadastroDepartamentos(),
        "cargos": CadastroCargo(),
        "grade": CadastroGrade(),
        "funcionarios": CadastroFuncionario(),
        "fornecedores": CadastroFonecedores(),
        "marcas": CadastroMarcas(),
        "modelos": CadastroModelos(),
        "classes": CadastroClasses(),
    }

    return forms[form]


def getform(form: str) -> Type[FlaskForm]:

    forms: dict[str, Type[FlaskForm]] = {
        "edit_equipamentos": EditItemProdutoForm(),
        "edit_estoque": EditSaldoGrade(),
        "edit_funcionarios": EditFuncionario(),
        "edit_empresas": EditEmpresa(),
        "edit_departamentos": EditDepartamentos(),
        "edit_cargos": EditCargo(),
        "edit_fornecedores": CadastroFonecedores(),
        "edit_marcas": CadastroMarcas(),
        "edit_modelos": CadastroModelos(),
        "edit_classes": CadastroClasses(),
        "edit_grade": CadastroGrade(),
    }

    return forms[form]
