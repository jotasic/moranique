from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegisterUserSerializer


class RegisterUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer