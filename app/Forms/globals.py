from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import app

permited_file = FileAllowed(['xlsx', 'xls'], 'Apenas arquivos ".xlsx" são permitidos!')


class IMPORTEPIForm(FlaskForm):
    
    arquivo = FileField(label="Arquivo de importação. Máximo 50Mb", validators=[FileRequired(), permited_file])
    submit = SubmitField(label="Importar")