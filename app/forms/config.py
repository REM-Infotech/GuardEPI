from os import abort

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length

from app.models import Groups, Users

file_allowed = FileAllowed(["jpg", "png", "jpeg"], "Images only!")


endpoints = [
    ("/epi", "EPI"),
    ("/config", "Configurações"),
    ("/corp", "Corporativo"),
    ("/estoque", "Estoque"),
]

perms = [
    ("CREATE", "Criar e Adicionar Itens"),
    ("READ", "Acessar Informações"),
    ("UPDATE", "Atualizar Informações"),
    ("DELETE", "Deletar Informações"),
]


def set_choicesUsers() -> list[tuple[str, str]]:
    return [(item.login, item.nome_usuario) for item in Users.query.all()]


def set_choicesGrupos() -> list[tuple[str, str]]:
    return [(item.name_group, item.name_group) for item in Groups.query.all()]


class FormUser(FlaskForm):
    nome = StringField(label="Nome", validators=[DataRequired()])
    login = StringField(label="Login", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(
        label="Senha", validators=[DataRequired(), Length(min=8, max=62)]
    )
    show_password = BooleanField("Exibir senha", id="check")
    submit = SubmitField(label="Criar")


class GroupForm(FlaskForm):

    try:
        nome = StringField(label="Nome do Grupo", validators=[DataRequired()])
        membros = SelectMultipleField("Selecione os Membros", choices=[])
        desc = TextAreaField("Descrição (Opcional)")

        def __init__(
            self,
            edit: bool = False,
            choices: list[tuple[str, str]] = None,
            *args,
            **kwargs
        ):
            super().__init__(*args, **kwargs)
            self.membros.choices.extend(set_choicesUsers())

    except Exception as e:
        abort(500, description=str(e))


class FormRoles(FlaskForm):
    name_rule = StringField(label="Nome da Regra", validators=[DataRequired()])
    grupos = SelectMultipleField("Selecione os Grupos", choices=[])
    rota = SelectField("Selecione a Página", choices=endpoints)
    permissoes = SelectMultipleField("Selecione as Permissões", choices=perms)
    desc = TextAreaField("Descrição (Opcional)")
    submit = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grupos.choices.extend(set_choicesGrupos())


class ProfileEditForm(FlaskForm):
    login = StringField(label="Usuário")
    nome_usuario = StringField(label="Nome Completo")
    old_password = PasswordField(label="Senha atual")
    new_password = PasswordField(label="Nova senha")
    email = EmailField(label="E-mail atual")
    filename = FileField(label="Foto de perfil", id="imagem", validators=[file_allowed])
    submit = SubmitField(label="Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
