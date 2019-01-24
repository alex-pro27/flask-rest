import datetime
from base64 import b64encode
from os import urandom

from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset import QuerySet
from werkzeug.wrappers import Response
import simplejson as json


def default_encoder(obj):
    if isinstance(obj, BaseDocument):
        return json_util._json_convert(obj.to_mongo())
    elif isinstance(obj, QuerySet):
        return json_util._json_convert(obj.as_pymongo())
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()


def JsonResponse(data, status=200, headers=None):

    return Response(
        json.dumps(data, default=default_encoder),
        content_type="application/json",
        status=status,
        headers=headers
    )


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def generate_password(length=8):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    chars = chars + chars.lower()
    return "".join(chars[ord(str(c)) % len(chars)] for c in b64encode(urandom(32)).decode('utf-8'))
