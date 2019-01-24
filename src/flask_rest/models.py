import binascii
import datetime
import os

import mongoengine

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import cached_property


class Role(mongoengine.Document):

    name = mongoengine.IntField(required=True, unique=True)
    permissions = mongoengine.ListField()
    meta = {'allow_inheritance': True}


class User(mongoengine.Document):

    firstname = mongoengine.StringField()
    lastname = mongoengine.StringField()
    login = mongoengine.StringField(unique=True)
    passwd = mongoengine.StringField(required=True)
    reg_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    role = mongoengine.ListField(mongoengine.ReferenceField(Role))
    active = mongoengine.BooleanField(default=True)

    meta = {'allow_inheritance': True}

    @cached_property
    def token(self):
        token = Token.objects(user_id=self.id).first()
        if not token:
            token = Token.objects.create(user=self)
        return token

    @property
    def full_name(self):
        return "{0} {1}".format(self.lastname, self.firstname)

    def set_passwd(self, passwd):
        self.passwd = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.passwd, passwd)


class TokenManager(mongoengine.QuerySet):

    def create(self, **kwargs):
        assert kwargs.get("user"), "Do not specify the user parameter"
        Token.objects(user_id=kwargs["user"].id).delete()
        def gen_token_key():
            token_key = Token.token_hex()
            if Token.objects(token_key=token_key).first():
                return gen_token_key()
            return token_key

        token = Token(user_id=kwargs["user"].id, token_key=gen_token_key())
        token.save()
        return token


class Token(mongoengine.Document):

    DEFAULT_ENTROPY = 32

    token_key = mongoengine.StringField(unique=True, required=True)
    user_id = mongoengine.ObjectIdField()

    meta = {'strict': False, 'queryset_class': TokenManager}

    @cached_property
    def user(self):
        return User.objects(id=self.user_id).first()

    @staticmethod
    def token_bytes(nbytes=None):
        if nbytes is None:
            nbytes = Token.DEFAULT_ENTROPY
        return os.urandom(nbytes)

    @staticmethod
    def token_hex(nbytes=None):
        return binascii.hexlify(Token.token_bytes(nbytes)).decode('ascii')
