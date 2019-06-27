from flask import (
    Blueprint, render_template, url_for
)
from models import Sound, Defaults

bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/')
def index():
    return render_template("schedules/index.html")


@bp.route('/create', methods=('GET', 'POST'))
def create():
    default_sound = Sound.objects(id=Defaults.objects.first().sound).first()
    return render_template("schedules/form.html", sounds=Sound.objects(), default_sound=default_sound)


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    return 'Hello World! Delete all teh things!'
