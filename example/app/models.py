import datetime
import mongoengine

from flask_rest.models import User


class GeoHistory(mongoengine.EmbeddedDocument):

    date = mongoengine.DateTimeField(default=datetime.datetime.now)
    coords = mongoengine.ListField() # Coords [latitude, longitude]


class AppUser(User):

    phone = mongoengine.StringField()
    coord_history = mongoengine.ListField(mongoengine.EmbeddedDocumentField(GeoHistory))
