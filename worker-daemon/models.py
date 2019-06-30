import mongoengine
from datetime import datetime


class Sound(mongoengine.Document):
    name = mongoengine.StringField(required=True, unique=True)
    filepath = mongoengine.StringField(unique=True)


class Bell(mongoengine.EmbeddedDocument):
    time = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    sound = mongoengine.ObjectIdField()


class Template(mongoengine.Document):
    name = mongoengine.StringField(required=True, unique=True)
    bells = mongoengine.EmbeddedDocumentListField(Bell)


class CustomSchedule(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    bells = mongoengine.EmbeddedDocumentListField(Bell)
    date = mongoengine.DateField(default=datetime.now().date, required=True, unique=True)


class Defaults(mongoengine.Document):
    sound = mongoengine.ObjectIdField()
    daily_templates = mongoengine.ListField(mongoengine.ObjectIdField())
