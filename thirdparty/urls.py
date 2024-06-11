from django.urls import path
from .views import CameraCheckAPIView
urlpatterns = [
    path('status', CameraCheckAPIView.as_view(), name='cam-status')
]
