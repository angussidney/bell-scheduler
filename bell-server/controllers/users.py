from flask import (
    Blueprint, render_template
)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/')
def list_users():
    return 'Hello World! List all users!'


@bp.route('/create', methods=('GET', 'POST'))
def edit():
    return 'Hello World! People making time!'


@bp.route('/<id>/edit', methods=('GET', 'POST'))
def edit(id):
    return 'Hello World! Editing time!'


@bp.route('/<id>/delete', methods=('POST',))
def index(id):
    return 'Hello World! Delete all teh people! DELETE! DELETE! DELETE!'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    return 'Hello World! Login page!'


@bp.route('/logout', methods=('POST',))
def logout():
    return 'Hello World! Logout page!'