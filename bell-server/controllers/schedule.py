from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, jsonify
)
from flask_security import login_required
from flask_login import current_user
from models import CustomSchedule, Bell, Sound, Defaults
from datetime import datetime, timedelta

bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/')
@login_required
def index():
    return render_template("schedules/index.html")


@bp.route('/list.json')
@login_required
def list_json():
    start = datetime.strptime(request.args['start'][:10], "%Y-%m-%d").date()
    end = datetime.strptime(request.args['end'][:10], "%Y-%m-%d").date()
    schedules = CustomSchedule.objects(date__gte=start, date__lt=end)
    return jsonify([{
        'id': str(s.id),
        'title': s.name,
        'start': s.date.strftime('%Y-%m-%d')
    } for s in schedules])


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == "POST":
        # TODO: Check that the date isn't in the past
        dates = zip(request.form.getlist('start'), request.form.getlist('end'))
        processed_dates = set()
        for start, end in dates:
            d1 = datetime.strptime(start, "%Y-%m-%d").date()
            d2 = datetime.strptime(end, "%Y-%m-%d").date()
            delta = d2 - d1
            for i in range(delta.days + 1):
                processed_dates.add(d1 + timedelta(days=i))

        for date in processed_dates:
            existing = CustomSchedule.objects(date=date)
            if existing:
                # TODO: Warn user before overwriting
                s = existing.first()
            else:
                s = CustomSchedule(date=date)

            s.name = request.form['name']

            times = request.form.getlist('bell_times')
            names = request.form.getlist('bell_names')
            sound_ids = [i if i != "default" else None
                         for i in request.form.getlist('bell_sound_ids')]
            s.bells = [Bell(time=b[0], name=b[1], sound=b[2])
                       for b in zip(times, names, sound_ids)]
            map(lambda bell: bell.save(), s.bells)

            s.save()

        flash('Custom schedule successfully created.', 'success')
        return redirect(url_for('schedule.index'))
    else:
        default_sound = Sound.objects(id=Defaults.objects.first().sound).first()
        return render_template("schedules/create.html", sounds=Sound.objects(), default_sound=default_sound)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/delete', methods=('POST',))
@login_required
def delete():
    start = datetime.strptime(request.form['start'][:10], "%Y-%m-%d").date()
    end = datetime.strptime(request.form['end'][:10], "%Y-%m-%d").date()
    schedules = CustomSchedule.objects(date__gte=start, date__lt=end)

    for schedule in schedules:
        schedule.delete()

    flash("Custom schedules successfully deleted.", "success")
    return redirect(url_for('schedule.index'))
