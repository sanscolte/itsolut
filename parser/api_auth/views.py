from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """API для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    """API для входа пользователя"""

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        """Функция для входа пользователя"""
        if not request.user.is_authenticated:
            username: str = request.data.get("username")
            password: str = request.data.get("password")
            user: User = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response(
                    {"message": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"message": "You login already"},
            status=status.HTTP_400_BAD_REQUEST,
        )
