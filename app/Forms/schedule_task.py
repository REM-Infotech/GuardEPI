from flask_wtf import FlaskForm
from pytz import all_timezones
from wtforms import (
    IntegerField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TimeField,
)
from wtforms.validators import DataRequired


class TaskNotificacaoForm(FlaskForm):
    nome_task = StringField(
        label="Nome da Task", validators=[DataRequired("Informe o nome da Task!!")]
    )

    hora_execucao = TimeField("Hora/Minuto da Execução")
    timezone = SelectField("Fuso horário", validators=[DataRequired()], choices=[])
    days_of_week = SelectMultipleField("Dias da Semana", choices=[])
    submit = SubmitField("Salvar Alterações")

    notify_vencimento = IntegerField(
        "Delta de dias", validators=[DataRequired()], default=60
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        timezones = [(timez, timez) for timez in all_timezones]
        self.timezone.choices.extend(timezones)
        self.days_of_week.choices.extend(
            [
                (0, "Domingo"),
                (1, "Segunda-Feira"),
                (2, "Terça-Feira"),
                (3, "Quarta-Feira"),
                (4, "Quinta-Feira"),
                (5, "Sexta-Feira"),
                (6, "Sábado"),
            ]
        )
