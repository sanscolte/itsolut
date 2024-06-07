from rest_framework import serializers

from api.models import Author, Advt


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Автора"""

    class Meta:
        model = Author
        fields = "__all__"


class AdvtSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Объявления"""

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Advt
        fields = "__all__"
