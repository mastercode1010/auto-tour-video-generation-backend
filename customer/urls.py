from django.urls import path
from .views import ClientRegistrationAPIView

urlpatterns = [
    path('client/add_with_photos', ClientRegistrationAPIView.as_view(), name='client_registration'),
]
