from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CharField


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    password: CharField = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data) -> User:
        """Метод регистрации пользователя"""
        user: User = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user
