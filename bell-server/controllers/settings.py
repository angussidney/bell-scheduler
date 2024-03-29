from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify, json
)
from flask import current_app as app
from flask_security import login_required, roles_required
from flask_login import current_user
from werkzeug.utils import secure_filename
from models import Template, Defaults, Sound, CustomSchedule
from helpers import check_file, weekdays
from datetime import datetime
import re
import os

bp = Blueprint('settings', __name__, url_prefix='/settings')


# weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


@bp.route('/templates', methods=('GET', 'POST'))
@login_required
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
@login_required
def list_sounds():
    return render_template("settings/sounds/list.html",
                           sounds=[(s.id, s.name, os.path.basename(s.filepath))
                                   for s in Sound.objects.order_by("+name")],
                           default=Defaults.objects.first().sound)


@bp.route('/sounds/create', methods=('GET', 'POST'))
@login_required
def create_sound():
    if request.method == 'POST':
        file = request.files["file"]
        if not (file and check_file(file, "wav")):
            flash("That filetype is not supported.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        # TODO: check if filename already exists, or is empty

        if any(Sound.objects(name=request.form['name'])):
            flash("There is already a bell sound with that name.", "error")
            return redirect(request.url)

        real_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "sounds", filename)
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
@login_required
def delete_sound(id):
    sound = Sound.objects(id=id).first()
    os.remove(sound.filepath)
    sound.delete()
    flash("Sound successfully deleted.", "success")
    return redirect(url_for('settings.list_sounds'))


@bp.route('/sounds/<id>/default', methods=('POST',))
@login_required
def default_sound(id):
    current_defaults = Defaults.objects.first()
    current_defaults.sound = id
    current_defaults.save()
    flash("Sound successfully set as default.", "success")
    return redirect(url_for('settings.list_sounds'))


# ----- #


@bp.route('/backups')
@login_required
@roles_required('admin')
def backups():
    return render_template("settings/backups/index.html")


@bp.route('/backups/import', methods=('POST',))
@login_required
@roles_required('admin')
def import_backup():
    file = request.files["file"]
    if not (file and check_file(file, "json")):
        flash("That filetype is not supported.", "error")
        return redirect(url_for("settings.backups"))

    filename = secure_filename(file.filename)
    if not re.match(r"^backup-\d{4}-\d{2}-\d{2}.json$", filename):
        flash("That doesn't look like a valid backup. Please only submit UNMODIFIED backups to the import function.",
              "error")
        return redirect(url_for("settings.backups"))

    # TODO: Make importing safer and more efficient
    real_filename = os.path.join(app.config['UPLOAD_FOLDER'], "imports", filename)
    file.save(real_filename)

    with open(real_filename) as f:
        d = json.load(f)

        # TODO: This probably messes up everyone else who is currently using the software.
        Sound.objects.delete()
        for s in d['sounds']:
            Sound.from_json(json.dumps(s)).save(force_insert=True)

        Template.objects.delete()
        for t in d['templates']:
            Template.from_json(json.dumps(t)).save(force_insert=True)

        CustomSchedule.objects.delete()
        for cs in d['schedules']:
            CustomSchedule.from_json(json.dumps(cs)).save(force_insert=True)

        Defaults.objects.delete()
        for df in d['defaults']:
            Defaults.from_json(json.dumps(df)).save(force_insert=True)

    flash("If you're seeing this message, it means that you followed all of the instructions correctly and nothing "
          "broke (hopefully). Congratulations!", "success")
    return redirect(url_for("settings.backups"))


@bp.route('/backups/export')
@login_required
@roles_required('admin')
def export_backup():
    # TODO: Surely we can be more efficient than jsonifying it, unjsonifying it, then jsonifying it again
    data = {
        'sounds': json.loads(Sound.objects.to_json()),
        'templates': json.loads(Template.objects.to_json()),
        'schedules': json.loads(CustomSchedule.objects.to_json()),
        'defaults': json.loads(Defaults.objects.to_json())
    }
    response = make_response(jsonify(data))
    response.headers["Content-Disposition"] = f"attachment; filename=backup-{str(datetime.now().date())}.json"
    return response
