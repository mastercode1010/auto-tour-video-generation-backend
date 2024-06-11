from django.urls import path
from .views import ClientRegistrationAPIView, ChildrenRegistrationAPIView, GetClientByIdAPIView, ClientDeleteAPIView, ClientUpdateAPIView, GetClientforVideoAPIView

urlpatterns = [
    path('add_client', ClientRegistrationAPIView.as_view(), name='client_registration'),
    path('add_child', ChildrenRegistrationAPIView.as_view(), name='add_child_with_photos'),
    path('getallclients', ClientRegistrationAPIView.as_view(), name='add_child_with_photos'),
    path('client/<int:pk>', GetClientByIdAPIView.as_view(), name='get-client-by-id'),
    path('delete', ClientDeleteAPIView.as_view(), name='user_delete'),
    path('update', ClientUpdateAPIView.as_view(), name='client-update'),
    path('getclientforvideo', GetClientforVideoAPIView.as_view(), name='get-clients-for-video'),
]
