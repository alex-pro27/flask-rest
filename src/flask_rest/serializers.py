import copy
import datetime
from _decimal import Decimal
from collections import OrderedDict
from mongoengine.fields import BaseField

from bson import ObjectId
from .helpers import add_metaclass


ALL_FIELDS = '__all__'


class Field(object):

    def bind(self, field_name, parent):
        self.field_name = field_name
        self.parent = parent

    def to_representation(self, instance):
        raise NotImplementedError()


class SerializerMethodField(Field):

    def __init__(self, method_name=None):
        self.method_name = method_name

    method_name = None

    def bind(self, field_name, parent):
        default_method_name = 'get_{field_name}'.format(field_name=field_name)

        if self.method_name is None:
            self.method_name = default_method_name

        super(SerializerMethodField, self).bind(field_name, parent)

    def to_representation(self, instance):
        method = getattr(self.parent, self.method_name)
        return method(instance)


class SerializerMetaclass(type):

    @classmethod
    def _get_declared_fields(cls, bases, attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]

        for base in reversed(bases):
            if hasattr(base, '_declared_fields'):
                fields = [
                             (field_name, obj) for field_name, obj
                             in base._declared_fields.items()
                             if field_name not in attrs
                         ] + fields

        return OrderedDict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)



@add_metaclass(SerializerMetaclass)
class ModelSerializer(Field):

    def __init__(self, query_set=None, many=False):
        self._cache = query_set
        self.many = many

    def to_representation(self, instance):
        self._cache = getattr(instance, self.field_name)
        return self.data

    def get_fields(self):
        return copy.deepcopy(self._declared_fields)

    def get_field_names(self, declared_fields):
        fields = getattr(self.Meta, 'fields', None)
        exclude = getattr(self.Meta, 'exclude', None)

        if fields and fields != ALL_FIELDS and not isinstance(fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple or "__all__". '
                'Got %s.' % type(fields).__name__
            )

        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                'The `exclude` option must be a list or tuple. Got %s.' %
                type(exclude).__name__
            )

        assert not (fields and exclude), (
            "Cannot set both 'fields' and 'exclude' options on "
            "serializer {serializer_class}.".format(
                serializer_class=self.__class__.__name__
            )
        )

        assert not (fields is None and exclude is None), (
            "Creating a ModelSerializer without either the 'fields' attribute "
            "or the 'exclude' attribute has been deprecated"
            "and is now disallowed. Add an explicit fields = '__all__' to the "
            "{serializer_class} serializer.".format(
                serializer_class=self.__class__.__name__
            ),
        )

        if fields == ALL_FIELDS:
            fields = None

        if fields is not None:
            required_field_names = set(declared_fields)
            for cls in self.__class__.__bases__:
                required_field_names -= set(getattr(cls, '_declared_fields', []))

            for field_name in required_field_names:
                assert field_name in fields, (
                    "The field '{field_name}' was declared on serializer "
                    "{serializer_class}, but has not been included in the "
                    "'fields' option.".format(
                        field_name=field_name,
                        serializer_class=self.__class__.__name__
                    )
                )
            return fields

        else:
            fields = self.get_all_fields()

        if exclude is not None:
            # If `Meta.exclude` is included, then remove those fields.
            for field_name in exclude:
                assert field_name in fields, (
                    "The field '{field_name}' was included on serializer "
                    "{serializer_class} in the 'exclude' option, but does "
                    "not match any model field.".format(
                        field_name=field_name,
                        serializer_class=self.__class__.__name__
                    )
                )
                fields.remove(field_name)

        return fields

    def get_model(self):
        return self.Meta.model

    def get_all_fields(self):
        return [
            field_name
            for field_name, value in self.get_model()._fields.items()
            if field_name != '_cls' and isinstance(value, BaseField)
        ]

    def default_encoder(self, value):
        if isinstance(value, ObjectId):
            return str(value)
        elif isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%dT%H:%M:%S")
        elif isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, Decimal):
            return str(value)
        return value

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = self.get_data()
        return self._data

    @property
    def fields(self):
        """
        A dictionary of {field_name: field_instance}.
        """
        if not hasattr(self, '_fields'):
            self._fields = OrderedDict()
            for key, value in self.get_fields().items():
                self._fields[key] = value
        return self._fields

    def get_data(self):
        model = self.get_model()

        def get_data(query_set):
            data, _data = OrderedDict(), dict()
            for key, cls_method in self.fields.items():
                cls_method.bind(key, self)
                _data[key] = cls_method.to_representation(query_set)

            for name_field in self.get_field_names(self.fields):
                if _data.get(name_field):
                    data[name_field] = self.default_encoder(_data.pop(name_field))
                elif hasattr(model, name_field):
                    value = getattr(query_set, name_field)
                    data[name_field] = self.default_encoder(value)
                else:
                    raise ValueError(
                        "not found field {field} on model {model}"
                            .format(field=name_field, model=model)
                    )
            return data

        if self.many:
            return [get_data(qs) for qs in self._cache]
        return get_data(self._cache)
