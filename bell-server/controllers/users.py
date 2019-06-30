from flask import (
    Blueprint, render_template, redirect, url_for, request, flash
)
from flask_security import login_required, roles_required, utils
from flask_login import current_user
from models import User
from xkcdpass import xkcd_password as xp

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/check_pwd')
@login_required
def check_password():
    if current_user.reset_required:
        flash("You have have requested a password reset. Please change your password now.", "info")
        return redirect(url_for('security.change_password'))
    else:
        print(current_user.reset_required)
        return redirect('/')


@bp.route('/successful_reset')
@login_required
def successful_reset():
    current_user.reset_required = False  # TODO: Handle redirects with next param
    current_user.save()
    return redirect('/')


# ----- #


@bp.route('/')
@login_required
@roles_required('admin')
def list_users():
    return render_template("users/index.html",
                           users=User.objects.order_by("+email"))


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def create():
    return "Text"


@bp.route('/<id>/reset', methods=('GET', 'POST'))
@login_required
@roles_required('admin')
def reset(id):
    wordfile = xp.locate_wordfile()
    words = xp.generate_wordlist(wordfile=wordfile, min_length=5, max_length=8)
    new_pwd = xp.generate_xkcdpassword(words, numwords=4)

    user = User.objects(id=id).first()
    user.password = utils.hash_password(new_pwd)
    user.reset_required = True
    user.save()
    return render_template("users/reset.html", password=new_pwd)


@bp.route('/<id>/delete', methods=('POST',))
@login_required
@roles_required('admin')
def delete(id):
    user = User.objects(id=id).first()
    user.delete()
    flash("User successfully deleted.", "success")
    return redirect(url_for('users.list_users'))
