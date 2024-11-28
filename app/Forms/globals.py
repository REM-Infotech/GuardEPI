from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField

permited_file = FileAllowed(["xlsx", "xls"], 'Apenas arquivos ".xlsx" são permitidos!')


class IMPORTEPIForm(FlaskForm):

    arquivo = FileField(
        label="Arquivo de importação. Máximo 50Mb",
        validators=[FileRequired(), permited_file],
    )
    submit = SubmitField(label="Importar")
