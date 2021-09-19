from django.db import models
from rest_framework.serializers import ModelSerializer

from api.users.models import User

class RegisterUserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('is_active', 'is_staff', 'date_of_join', 'last_login', 'is_active', 'is_admin', 'id')
        extra_kwargs = {'password' : {'write_only' : True}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)