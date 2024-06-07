from django.core.management import call_command
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Advt
from api.serializers import AdvtSerializer


class AdvtDetailView(generics.RetrieveAPIView):
    queryset = Advt.objects.all()
    serializer_class = AdvtSerializer
    permission_classes = [IsAuthenticated]


class ParseAdsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            call_command('parse_ads')
            return Response(
                {"status": "success", "message": "Ads parsed successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
