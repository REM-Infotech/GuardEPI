from typing import Type

from flask_wtf import FlaskForm

from app import db
from app.Forms import (
    CadastroCargo,
    CadastroClasses,
    CadastroDepartamentos,
    CadastroEmpresa,
    CadastroEPIForm,
    CadastroFonecedores,
    CadastroFuncionario,
    CadastroGrade,
    CadastroMarcas,
    CadastroModelos,
    InsertEstoqueForm,
)
from app.Forms.edit import (
    EditCargo,
    EditDepartamentos,
    EditEmpresa,
    EditFuncionario,
    EditItemProdutoForm,
    EditSaldoGrade,
)
from app.models import (
    Cargos,
    ClassesEPI,
    Departamento,
    Empresa,
    EstoqueEPI,
    EstoqueGrade,
    Fornecedores,
    Funcionarios,
    GradeEPI,
    Groups,
    Marcas,
    ModelosEPI,
    ProdutoEPI,
    RegistroEntradas,
    RegistrosEPI,
    Users,
)

tipo = db.Model


def get_models(tipo: str) -> Type[tipo]:
    models = {
        "equipamentos": ProdutoEPI,
        "estoque": EstoqueEPI,
        "grade": GradeEPI,
        "empresas": Empresa,
        "funcionarios": Funcionarios,
        "departamentos": Departamento,
        "cargo_bp.cargos": Cargos,
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
        "cargo_bp.cargos": CadastroCargo(),
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
