from flask import request
from .exceptions import MethodNotAllowed


class BaseView(object):

    decorators = ()
    request = None

    @classmethod
    def as_view(cls, params=None, *class_args, **class_kwargs):

        def view(*args, **kwargs):
            self = view.view_class(*class_args, **class_kwargs)
            self.request = request

            if params:
                method, view_name = list(params.items())[0]
                if request.method.upper() == method.upper():
                    view_func = getattr(self, view_name)
                else:
                    raise MethodNotAllowed()
            else:
                view_func = getattr(self, request.method.lower())
            return view_func(request, *args, **kwargs)

        if cls.decorators:
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)

        name = cls.__name__
        if params:
            name = "%s->%s" % (name, list(params.values())[0])

        view.view_class = cls
        view.__name__ = name
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        return view
