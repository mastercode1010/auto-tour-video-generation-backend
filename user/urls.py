from django.urls import path
from .views import UserRegistrationAPIView, UserLoginAPIView, PasswordResetRequestAPIView, PasswordResetAPIView, UserDeleteAPIView, UserUpdateAPIView, UserRangeListAPIView, GetUserByIdAPIView

urlpatterns = [
    path('register', UserRegistrationAPIView.as_view(), name='auth_register'),
    path('login', UserLoginAPIView.as_view(), name='auth_login'),
    path('password_reset', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('reset/<uidb64>/<token>', PasswordResetAPIView.as_view(), name='password_reset'),
    path('delete', UserDeleteAPIView.as_view(), name='user_delete'),
    path('update', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/range', UserRangeListAPIView.as_view(), name='user-range-list'),
    path('user/<int:pk>', GetUserByIdAPIView.as_view(), name='get-user-by-id')
]
