from rest_framework import serializers
from api.models import Post
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    date=serializers.DateTimeField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Post
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","password","first_name","last_name","email"]