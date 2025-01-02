import random
import string
import unicodedata

# Função para formatar como moeda brasileira
import babel.numbers as numbers
import bcrypt
from babel.dates import format_date
from flask_sqlalchemy.model import Model

from app.misc.generate_doc import (
    add_watermark,
    adjust_image_transparency,
    create_EPI_control_sheet,
    create_watermark_pdf,
)

salt = bcrypt.gensalt()
__all__ = (
    create_EPI_control_sheet,
    create_watermark_pdf,
    add_watermark,
    adjust_image_transparency,
)


def format_currency_brl(value: int | float | str) -> str:
    number = numbers.format_currency(value, "BRL", locale="pt_BR")
    number = unicodedata.normalize("NFKD", number)
    return number


# Função para formatar a data e obter o nome do mês em português
def format_date_brl(date):
    return format_date(date, format="MMMM", locale="pt_BR").capitalize()


def generate_pid(count: int = 6) -> str:
    while True:
        # Gerar 4 letras maiúsculas e 4 dígitos
        letters = random.sample(string.ascii_uppercase, 6)
        digits = random.sample(string.digits, 6)

        # Intercalar letras e dígitos
        pid = "".join(
            [letters[i // 2] if i % 2 == 0 else digits[i // 2] for i in range(count)]
        )

        # Verificar se a string gerada não contém sequências do tipo "AABB"
        if not any(pid[i] == pid[i + 1] for i in range(len(pid) - 1)):
            return pid


def hash_str() -> str:
    return bcrypt.hashpw(generate_pid().encode(), salt).decode("utf-8")


def get_models(tipo: str) -> Model:

    from ..models import (
        Cargos,
        ClassesEPI,
        Departamento,
        Empresa,
        EstoqueEPI,
        EstoqueGrade,
        Funcionarios,
        GradeEPI,
        ProdutoEPI,
        RegistroEntradas,
        RegistrosEPI,
    )
    from ..models.users import Groups, Users

    modelo = {
        "categorias": ClassesEPI,
        "equipamentos": ProdutoEPI,
        "grades": GradeEPI,
        "estoque": EstoqueEPI,
        "estoque_grade": EstoqueGrade,
        "entradas": RegistroEntradas,
        "cautelas": RegistrosEPI,
        "funcionarios": Funcionarios,
        "empresas": Empresa,
        "departamentos": Departamento,
        "cargo.cargos": Cargos,
        "users": Users,
        "groups": Groups,
    }

    model = modelo.get(tipo)
    if model is None:
        message = "".join(("Modelo ", f'"{tipo}"', " não encontrado."))
        raise AttributeError(message)

    return model
