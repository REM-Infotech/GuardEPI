from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired


class TaskNotificacaoForm(FlaskForm):

    nome_task: StringField = StringField(
        label="Nome da Task", validators=[DataRequired("Informe o nome da Task!!")]
    )
    periodicidade_dia: IntegerField = IntegerField("Contagem de dias para exeutar")
    periodicidade_semana: SelectMultipleField = SelectMultipleField(
        "Selecione os dias da semana",
        choices=[
            (1, "Domingo"),
            (2, "Segunda-Feira"),
            (3, "Terça-Feira"),
            (4, "Quarta-Feira"),
            (5, "Quinta-Feira"),
            (6, "Sexta-Feira"),
            (7, "Sábado"),
        ],
    )

    contagem_dias_notificacao: IntegerField = IntegerField(
        "Delta de dias para o inicio da tarefa"
    )

    submit = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass
