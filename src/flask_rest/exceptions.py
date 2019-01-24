# from enum import Enum
from werkzeug.exceptions import HTTPException
from werkzeug.utils import escape

from .helpers import default_encoder
import simplejson as json


class HTTPError(HTTPException):

    headers = ()

    def get_body(self, environ=None):
        return json.dumps(
            dict(
                code=self.code,
                name=escape(self.name),
                description=self.get_description(environ)
            ),
            default=default_encoder
        )

    def get_description(self, environ=None):
        """Get the description."""
        return escape(self.description)

    def get_headers(self, environ=None):
        """Get a list of headers."""
        headers = [('Content-Type', 'application/json')]
        if self.headers:
            headers.extend(self.headers)
        return headers


class MethodNotAllowed(HTTPError):
    code = 405
    description = 'Method not Allowed, 405'


class NotFound(HTTPError):
    message = 'Not found, 404'
    description = 404


class Unauthorized(HTTPError):
    description = "Unauthorized, 401"
    code = 401
    headers = (
        ('WWW-Authenticate', 'Basic realm="Login Required"'),
    )


class TokenUnauthorized(Unauthorized):
    headers = ()


class Forbidden(HTTPError):
    description = "Permission denied, 403"
    code = 403

