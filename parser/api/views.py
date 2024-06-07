from typing import List

from django.core.management import call_command
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Advt
from api.serializers import AdvtSerializer


class AdvtDetailView(generics.RetrieveAPIView):
    """
    API для получения деталей объявления. Доступно только авторизованным пользователям
    """

    queryset = Advt.objects.all()
    serializer_class = AdvtSerializer
    permission_classes = [IsAuthenticated]


class ParseAdsView(APIView):
    """
    API для парсинга объявлений. Доступно только авторизованным пользователям.
    Может работать некорректно из-за ограничений reCAPTCHA на сайте
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None) -> Response:
        """
        Функция парсинга объявлений и их получения
        :param request: Запрос
        :param format: Формат
        :return: Последние 10 объявлений
        """
        call_command("parse_ads")
        latest_ads: List[Advt] = Advt.objects.all().order_by("-id")[:7]
        serializer: AdvtSerializer = AdvtSerializer(latest_ads, many=True)
        return Response(
            {"data": serializer.data},
            status=status.HTTP_200_OK,
        )
