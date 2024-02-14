from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, PasswordResetRequestAPIView, PasswordResetAPIView

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='auth_register'),
    path('login', UserLoginAPIView.as_view(), name='auth_login'),
    path('password_reset', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('reset/<uidb64>/<token>', PasswordResetAPIView.as_view(), name='password_reset'),
]
