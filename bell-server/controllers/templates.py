from flask import (
    Blueprint, redirect, render_template, request, url_for, flash
)
from models import Bell, Template, Sound, Defaults

bp = Blueprint('templates', __name__, url_prefix='/templates')


@bp.route('/')
def index():
    return render_template("templates/index.html",
                           templates=Template.objects.order_by("+name"),
                           defaults=Defaults.objects.first().daily_templates)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        t = Template()
        t.name = request.form['name']

        times = request.form.getlist('bell_times')
        names = request.form.getlist('bell_names')
        sound_ids = [i if i != "default" else None
                     for i in request.form.getlist('bell_sound_ids')]

        t.bells = [Bell(time=b[0], name=b[1], sound=b[2])
                   for b in zip(times, names, sound_ids)]
        map(lambda bell: bell.save(), t.bells)
        t.save()

        if bool(request.form.get('apply', False)):
            default = Defaults.objects.first()
            selected_days = request.form.getlist('apply_to')
            for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
                if day in selected_days:
                    default.daily_templates[i] = t.id
            default.save()

        return redirect(url_for('templates.index'))
    else:
        default_sound = Sound.objects(id=Defaults.objects.first().sound).first()
        return render_template('templates/create.html', sounds=Sound.objects(), default_sound=default_sound)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    template = Template.objects(id=id).first()
    template.delete()
    flash("Template successfully deleted.", "success")
    return redirect(url_for('templates.index'))
