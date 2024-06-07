from django.urls import path

from api_auth.views import RegisterView, LoginView

app_name = 'api_auth'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
