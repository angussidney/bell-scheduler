from flask import (
    Blueprint, redirect, render_template, request, url_for
)
from models import Bell, Template, Sound

bp = Blueprint('templates', __name__, url_prefix='/templates')


@bp.route('/')
def index():
    return 'Hello World! List all of the templates!'


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        t = Template()
        t.name = request.form['name']

        times = request.form.getlist('bell_times')
        names = request.form.getlist('bell_names')
        # TODO Request sound objects from database, then match up to sound names
        t.bells = [Bell(time=b[0], name=b[1]) for b in zip(times, names)]

        t.save()

        if bool(request.form.get('apply', False)):
            days = request.form.getlist('apply_to')
            # TODO loop through days and add to settings

        return redirect(url_for('.show'))
    else:
        return render_template('templates/create.html')


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/<id>/delete', methods=('POST',))
def index(id):
    return 'Hello World! Delete all teh things!'
