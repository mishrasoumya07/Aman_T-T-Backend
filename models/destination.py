from mongoengine import *

class Destination(Document):
    name = StringField(required=True)
    location = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    duration = IntField(required=True)
    image = StringField(required=True)
    activities = ListField(StringField())

    meta = {
        "collection": "destination"
    }