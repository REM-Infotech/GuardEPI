from os import path
from pathlib import Path

from flask import Blueprint, render_template

from ...Forms import schedule_task

template_folder = path.join(Path(__file__).parent.resolve(), "templates")
schedule_bp = Blueprint(
    "schedules", __name__, url_prefix="/schedule", template_folder=template_folder
)


@schedule_bp.get("/dash")
def dash():
    form = schedule_task.TaskNotificacaoForm()
    page = "schedules.html"
    return render_template("index.html", page=page, form=form)
