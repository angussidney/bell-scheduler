from flask_mongoengine import MongoEngine
from datetime import datetime

db = MongoEngine()


class Sound(db.Document):
    name = db.StringField(required=True)
    filepath = db.StringField()


class Bell(db.EmbeddedDocument):
    time = db.StringField(required=True)
    name = db.StringField(required=True)
    sound = db.ObjectIdField()


class Template(db.Document):
    name = db.StringField(required=True)
    bells = db.EmbeddedDocumentListField(Bell)


class CustomSchedule(db.Document):
    name = db.StringField(required=True)
    bells = db.EmbeddedDocumentListField(Bell)
    date = db.DateField(default=datetime.now().date, required=True)


class Defaults(db.Document):
    sound = db.ObjectIdField()
    daily_templates = db.ListField(db.ObjectIdField())
