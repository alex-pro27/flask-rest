import re


def create_decorator_register_url():
    """
    creates a decorator for the View class
    Will generate the Url named method with the name on the form:
    def get__ <- Method request, some_method__ <- method Name id__ <- option
    example:

    view.py:
        ...
        register_url = create_decorator_register_url()

        @register_url
        class SomeView(ViewSet)

            def get__some_method__name__id(self, request, name, id):
                return Response({'id': id, 'name': name})

            get__some_method__name__id.annotate = [("id": int), ("name": str),]

    --*--

    urls.py:
        ...
        from .views import register_url
        urlpatterns = register_url.all

    --*--

    register_url.all -> [
        (
            "/some-method/:name/:id",
            SomeView.as_view({'get': 'get__some_method__name__id'}),
        )
    ]
    """
    urls = []

    def register_url(cls):
        for key, val in cls.__dict__.items():
            request_method = re.match(r"^(post|get|put|delete)__", key)
            if request_method:
                name = key.replace(request_method.group(), "")

                _url = name.replace("__", "/").replace("_", "-")

                if getattr(val, "annotate", None):
                    for _value in val.annotate:
                        _url = _url.replace(_value, ":%s" % _value)

                request_method = request_method.groups()[0]
                urls.append(
                    (_url,  cls.as_view({request_method: key}),),
                )

        return cls
    register_url.all = urls
    return register_url
