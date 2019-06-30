from flask_mongoengine import MongoEngine
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = MongoEngine()


class Sound(db.Document):
    name = db.StringField(required=True, unique=True)
    filepath = db.StringField(unique=True)


class Bell(db.EmbeddedDocument):
    time = db.StringField(required=True)
    name = db.StringField(required=True)
    sound = db.ObjectIdField()


class Template(db.Document):
    name = db.StringField(required=True, unique=True)
    bells = db.EmbeddedDocumentListField(Bell)


class CustomSchedule(db.Document):
    name = db.StringField(required=True)
    bells = db.EmbeddedDocumentListField(Bell)
    date = db.DateField(default=datetime.now().date, required=True, unique=True)


class Defaults(db.Document):
    sound = db.ObjectIdField()
    daily_templates = db.ListField(db.ObjectIdField())


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    email = db.StringField(max_length=255, unique=True)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    reset_required = db.BooleanField(default=True)
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
