from functools import wraps
from flask import request
from .exceptions import Unauthorized, TokenUnauthorized
from .models import User, Token


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    user = User.objects(login=username).first()
    if user:
        if user.check_passwd(password):
            request.user = user
            return True
    return False


def check_auth_token(token):
    _token = Token.objects(token_key=token).first()
    if _token:
        request.user = _token.user
        return True
    return False


def requires_auth(f):
    """ Check basic or token auth """
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        is_auth = False
        if auth and auth.type == 'basic':
            is_auth = check_auth(auth.username, auth.password)
        else:
            auth_header = request.headers.environ.get('HTTP_AUTHORIZATION')
            if auth_header and 'Token' in auth_header:
                token = auth_header.replace("Token ", "")
                is_auth = check_auth_token(token)
        if is_auth:
            return f(*args, **kwargs)
        raise Unauthorized()
    return wrapper


def basic_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if auth and auth.type == 'basic':
            if check_auth(auth.username, auth.password):
                return f(*args, **kwargs)
        raise Unauthorized()
    return wrapper


def token_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.environ.get('HTTP_AUTHORIZATION')
        if auth_header and 'Token' in auth_header:
            token = auth_header.replace("Token ", "")
            if check_auth_token(token):
                return f(*args, **kwargs)
        raise TokenUnauthorized()
    return wrapper
