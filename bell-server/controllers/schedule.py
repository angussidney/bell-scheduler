from flask import (
    Blueprint, render_template
)

bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/')
def index():
    return 'Hello World! List all of the schedules!'


@bp.route('/create', methods=('GET', 'POST'))
def create():
    return 'Hello World! Lets create a schedule!'


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/<id>/delete', methods=('POST',))
def delete(id):
    return 'Hello World! Delete all teh things!'
