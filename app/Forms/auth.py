from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):

    login = StringField(label="Login", description="Login", validators=[DataRequired()])
    password = PasswordField(
        label="Senha", description="Senha", validators=[DataRequired()]
    )
    keep_login = BooleanField(label="Manter login")
    submit = SubmitField(label="Entrar")
