from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from flask import current_app as app
from werkzeug.utils import secure_filename
from models import Template, Defaults
from helpers import check_file
import os

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/templates', methods=('GET', 'POST'))
def templates():
    return render_template('settings/templates/index.html',
                           templates=Template.objects(),
                           defaults=Defaults.objects.first().daily_templates)


# ----- #


@bp.route('/sounds')
def list_sounds():
    return "Hello World! Beep, boop, bip bip bip!"


@bp.route('/sounds/create', methods=('GET', 'POST'))
def create_sound():
    if request.method == 'POST':
        file = request.files["file"]
        if file and check_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('list_sounds'))
        else:
            flash("That filetype is not supported.")
            return redirect(request.url)
    else:
        return render_template("settings/sounds/create.html")


@bp.route('/sounds/<id>/delete', methods=('POST',))
def delete_sound(id):
    return "Hello World! Sad sound :("


@bp.route('/sounds/default', methods=('POST',))
def default_sound():
    return "Hello World is the default starting program!"


# ----- #


@bp.route('/backups')
def backups():
    return "Hello World! Don't forget to backup!"


@bp.route('/backups/import', methods=('POST',))
def import_backup():
    return "Hello World! Don't forget to actually use your backups!"


@bp.route('/backups/export')
def export_backup():
    return "Hello World! Don't forget to actually do your backups!"
