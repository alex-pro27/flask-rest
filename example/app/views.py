from flask import render_template
from functools import wraps

from werkzeug.wrappers import BaseResponse

from .exceptions import AppError
from .serializers import ApiUserSerializer
from flask_rest.authentication import requires_auth
from flask_rest.decorators import create_decorator_register_url
from flask_rest.helpers import JsonResponse
from flask_rest.views import BaseView
from .models import AppUser


register_url = create_decorator_register_url()


def handler_error(method):
    @wraps(method)
    def wrap(*args, **kwargs):
        _response = None
        try:
            _response = method(*args, **kwargs)
        except AppError as e:
            _response = JsonResponse(
                dict(
                    message=e.message,
                    code=e.code
                )
            )
        if isinstance(_response, BaseResponse):
            return _response
        else:
            return JsonResponse(_response)
    return wrap


class TestChatView(BaseView):

    def get(self, request):
        return render_template('test.html')


@register_url
class UserViewSet(BaseView):

    decorators = (requires_auth, handler_error,)

    def get__user(self, request):
        user: AppUser = request.user
        return ApiUserSerializer(user).data

    def get__users(self, request):
        users = AppUser.objects()
        return ApiUserSerializer(users, many=True).data
