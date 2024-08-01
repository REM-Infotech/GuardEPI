from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ForgotPassword(FlaskForm):
    
    email_recover = StringField(label="E-mail para recuperar senha", validators=[DataRequired()])
    submit = SubmitField(label="Recuperar senha")
    
class ByPassRecover(FlaskForm):
    
    codigoverificar = StringField(label="Código de verificação", validators=[DataRequired(), Length(min=6, max=6)])
    new_senha = StringField(label="Nova Senha", validators=[DataRequired(), Length(min=8, max=62)])
    repeat_senha = StringField(label="Repetir Senha", validators=[DataRequired(), Length(min=8, max=62)])
    submit = SubmitField(label="Alterar senha!")