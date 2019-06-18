from flask import (
    Blueprint, render_template
)

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/', methods=('GET', 'POST'))
def settings():
    return render_template('settings/index.html')


@bp.route('/backups')
def backups():
    return "Hello World! Don't forget to backup!"


@bp.route('/backups/import', methods=('POST',))
def backups():
    return "Hello World! Don't forget to actually use your backups!"


@bp.route('/backups/export')
def backups():
    return "Hello World! Don't forget to actually do your backups!"
