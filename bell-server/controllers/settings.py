from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from flask import current_app as app
from werkzeug.utils import secure_filename
from models import Template, Defaults, Sound
from helpers import check_file
import os

bp = Blueprint('settings', __name__, url_prefix='/settings')

weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@bp.route('/templates', methods=('GET', 'POST'))
def templates():
    if request.method == "POST":
        new_defaults = [request.form[day] for day in weekdays]
        defaults = Defaults.objects.first()
        defaults.daily_templates = new_defaults
        defaults.save()
        flash("Default templates successfully updated.", "success")
        return redirect(url_for("templates.index"))
    else:
        return render_template('settings/templates/index.html',
                               templates=Template.objects(),
                               defaults=Defaults.objects.first().daily_templates,
                               days=enumerate(weekdays))


# ----- #


@bp.route('/sounds')
def list_sounds():
    return render_template("settings/sounds/list.html",
                           sounds=[(s.id, s.name, os.path.basename(s.filepath))
                                   for s in Sound.objects.order_by("+name")],
                           default=Defaults.objects.first().sound)


@bp.route('/sounds/create', methods=('GET', 'POST'))
def create_sound():
    if request.method == 'POST':
        file = request.files["file"]
        if not (file and check_file(file)):
            flash("That filetype is not supported.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        # TODO: check if filename already exists, or is empty

        if any(Sound.objects(name=request.form['name'])):
            flash("There is already a bell sound with that name.", "error")
            return redirect(request.url)

        real_filepath = os.path.join(app.instance_path, filename)
        file.save(real_filepath)
        sound = Sound(name=request.form['name'], filepath=real_filepath)
        sound.save()

        if bool(request.form.get('default', False)):
            current_defaults = Defaults.objects.first()
            current_defaults.sound = sound.id
            current_defaults.save()
            flash("Sound successfully created and set as default.", "success")
        else:
            flash("Sound successfully created.", "success")
        return redirect(url_for('settings.list_sounds'))
    else:
        return render_template("settings/sounds/create.html")


@bp.route('/sounds/<id>/delete', methods=('POST',))
def delete_sound(id):
    sound = Sound.objects(id=id).first()
    os.remove(sound.filepath)
    sound.delete()
    flash("Sound successfully deleted.", "success")
    return redirect(url_for('settings.list_sounds'))


@bp.route('/sounds/<id>/default', methods=('POST',))
def default_sound(id):
    current_defaults = Defaults.objects.first()
    current_defaults.sound = id
    current_defaults.save()
    flash("Sound successfully set as default.", "success")
    return redirect(url_for('settings.list_sounds'))


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
