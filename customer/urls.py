from django.urls import path
from .views import ClientRegistrationAPIView, ChildrenRegistrationAPIView

urlpatterns = [
    path('client/add_with_photos', ClientRegistrationAPIView.as_view(), name='client_registration'),
    path('child/add_with_photos', ChildrenRegistrationAPIView.as_view(), name='add_child_with_photos'),
    path('getallclients', ClientRegistrationAPIView.as_view(), name='add_child_with_photos'),
]
