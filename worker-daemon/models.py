from mongoengine import *
from datetime import datetime


class Sound(Document):
    name = StringField(required=True)
    filepath = StringField()


class Bell(EmbeddedDocument):
    time = StringField(required=True)
    name = StringField(required=True)
    sound = ObjectIdField()


class BellSchedule(Document):
    name = StringField(required=True)  # Human readable name
    bells = EmbeddedDocumentListField(Bell)

    meta = {'allow_inheritance': True}


class Template(Document):
    pass


class CustomSchedule(Document):
    date = DateField(default=datetime.now().date, required=True)


class Defaults(Document):
    sound = ObjectIdField()
    daily_templates = ListField(ObjectIdField())
