from rest_framework import serializers
from .models import Values
from django.contrib.auth.models import User
class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = [
            'integer',
        ]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username'
        ]