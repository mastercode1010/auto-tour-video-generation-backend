from django.urls import path
from .views import ClientRegistrationAPIView, ChildrenRegistrationAPIView, GetClientByIdAPIView, ClientDeleteAPIView, ClientUpdateAPIView

urlpatterns = [
    path('client/add_with_photos', ClientRegistrationAPIView.as_view(), name='client_registration'),
    path('child/add_with_photos', ChildrenRegistrationAPIView.as_view(), name='add_child_with_photos'),
    path('getallclients', ClientRegistrationAPIView.as_view(), name='add_child_with_photos'),
    path('client/<int:pk>', GetClientByIdAPIView.as_view(), name='get-client-by-id'),
    path('delete', ClientDeleteAPIView.as_view(), name='user_delete'),
    path('update', ClientUpdateAPIView.as_view(), name='client-update'),
]
