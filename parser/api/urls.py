from django.urls import path

from api.views import AdvtDetailView, ParseAdsView

app_name = 'api'

urlpatterns = [
    path('ad/<int:pk>/', AdvtDetailView.as_view(), name='ad-detail'),
    path('parse/', ParseAdsView.as_view(), name='ads-parse'),
]
