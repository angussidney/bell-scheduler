from flask import (
    Blueprint, render_template
)
from flask_security import login_required
from flask_login import current_user
from models import CustomSchedule, Defaults, Template
from helpers import weekdays
from datetime import datetime

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    date = datetime.now()
    today = CustomSchedule.objects(date=date.date()).first()
    if not today:
        temp_id = Defaults.objects().first().daily_templates[date.weekday()]
        today = Template.objects(id=temp_id).first()

    processed_bells = []
    found_active = False
    for bell in today.bells:
        time = datetime.strptime(bell.time, "%H:%M").time()
        if time > date.time():
            if not found_active:
                processed_bells.append((bell, 'next'))
                found_active = True
            else:
                processed_bells.append((bell, 'later'))
        else:
            processed_bells.append((bell, 'earlier'))

    if 4 <= date.day <= 20 or 24 <= date.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][date.day % 10 - 1]

    return render_template("dashboard/index.html",
                           datestring=date.strftime("%A %-d{} %B %Y".format(suffix)),
                           bells=processed_bells,
                           schedule=today.name)
