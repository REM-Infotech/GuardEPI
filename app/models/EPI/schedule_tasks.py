from app import db


class TaskNotificacao(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, unique=True)
    nome_task: str = db.Column(db.String(length=64), nullable=False)
    periodicidade_dia: int = db.Column(db.Integer, nullable=False, default=1)
    periodicidade_semana: int = db.Column(db.Integer, nullable=False, default=1)

    contagem_dias_notificacao: int = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, nome_task: str, periodicidade: int) -> None:
        self.nome_task = nome_task
        self.periodicidade = periodicidade
