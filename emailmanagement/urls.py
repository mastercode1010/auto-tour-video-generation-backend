from django.urls import path
from .views import ExitEmailSendListCreateAPIView, ExitEmailSendDetailAPIView, ExitEmailSendDeleteAPIView

urlpatterns = [
    path('add', ExitEmailSendListCreateAPIView.as_view(), name='ExitEmailSend_registeration'),
    path('get/all', ExitEmailSendListCreateAPIView.as_view(), name='get_all_coloring_pages'),
    path('get/<int:pk>', ExitEmailSendDetailAPIView.as_view(), name='get-ExitEmailSend-by-id'),
    path('delete', ExitEmailSendDeleteAPIView.as_view(), name='ExitEmailSend_delete'),
    path('update', ExitEmailSendDetailAPIView.as_view(), name='ExitEmailSend-update'),
]
