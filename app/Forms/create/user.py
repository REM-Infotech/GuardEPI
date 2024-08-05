from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, PasswordField,
                     DateField, IntegerField, BooleanField, EmailField, TextAreaField, SelectMultipleField)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length


class CreateUserForm(FlaskForm):

    nome = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Senha", validators=[
                             DataRequired(), Length(min=8, max=62)])
    show_password = BooleanField('Exibir senha', id='check')
    submit = SubmitField(label="Criar")
