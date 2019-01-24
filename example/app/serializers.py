from flask_rest.serializers import ModelSerializer, SerializerMethodField
from .models import AppUser


class ApiUserSerializer(ModelSerializer):

    full_name = SerializerMethodField()
    token = SerializerMethodField()

    class Meta:
        model = AppUser
        fields = ('id', 'full_name', 'phone', 'login', 'reg_date', 'active', 'token',)

    def get_full_name(self, obj):
        return obj.full_name

    def get_token(self, obj):
        return obj.token.token_key
