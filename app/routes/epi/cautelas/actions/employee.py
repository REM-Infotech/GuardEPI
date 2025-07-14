from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from quart import current_app as app

from app.forms.epi import Cautela
from app.models.Funcionários import Empresa, Funcionarios


async def employee_info(
    form: Cautela, db: SQLAlchemy
) -> tuple[Path, Funcionarios | None]:
    funcionario_data = (
        db.session.query(Funcionarios)
        .filter(Funcionarios.nome_funcionario == form.funcionario.data)
        .first()
    )

    nome_empresa = funcionario_data.empresa
    empresa_data = (
        db.session.query(Empresa).filter(Empresa.nome_empresa == nome_empresa).first()
    )
    image_data = empresa_data.blob_doc
    original_path = Path(app.config["IMAGE_TEMP_PATH"]).joinpath(empresa_data.filename)

    with original_path.open("wb") as f:
        f.write(image_data)

    return original_path, funcionario_data
