from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import Length, DataRequired
from flask_wtf.file import FileField, FileAllowed

file_allowed = FileAllowed(["jpg", "png", "jpeg"], "Images only!")


class ProfileEditForm(FlaskForm):

    login = StringField(label="Usuário")
    nome_usuario = StringField(label="Nome Completo")
    old_password = PasswordField(label="Senha atual")
    new_password = PasswordField(label="Nova senha")
    email = EmailField(label="E-mail atual")
    filename = FileField(label="Foto de perfil", id="imagem", validators=[file_allowed])
    submit = SubmitField(label="Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)


class AdmChangePassWord(FlaskForm):

    user_to_change = StringField(
        label="Usuário para a troca de senha", validators=[DataRequired()]
    )
    new_password = PasswordField(
        label="Nova senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    repeat_password = PasswordField(
        label="Repetir senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    submit_password = SubmitField(label="Alterar senha!")


class AdmChangeEmail(FlaskForm):

    user_to_change = StringField(
        label="Usuário para a troca de email", validators=[DataRequired()]
    )
    new_email = StringField(label="Novo e-mail", validators=[DataRequired()])
    repeat_email = StringField(label="Repetir e-mail", validators=[DataRequired()])
    submit_email = SubmitField(label="Alterar e-mail!")


class ChangePassWord(FlaskForm):

    old_password = PasswordField(
        label="Senha atual", validators=[DataRequired(), Length(min=8, max=62)]
    )
    new_password = PasswordField(
        label="Nova senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    repeat_password = PasswordField(
        label="Repetir senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    submit_password = SubmitField(label="Alterar senha!")


class ChangeEmail(FlaskForm):

    old_email = EmailField(label="E-mail atual", validators=[DataRequired()])
    new_email = EmailField(label="Novo e-mail", validators=[DataRequired()])
    repeat_email = EmailField(label="Novo e-mail", validators=[DataRequired()])
    submit_email = SubmitField(label="Alterar e-mail!")
