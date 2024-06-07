from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Author, Advt


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AdvtSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Advt
        fields = '__all__'
