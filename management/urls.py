from django.urls import path
from .views import HeaderAPIView, HeaderAddAPIView, HeaderDeleteAPIView, FooterAddAPIView, FooterAPIView, FooterDeleteAPIView, CameraVoiceAPIView, CameraVoiceByCameraIdAPIView, GetAllCameraVoiceAPIView, DeleteCameraVoiceAPIView, UpdateCameraVoiceAPIView, CameraAPIView, CameraDeleteAPIView, CameraUpdateAPIView

urlpatterns = [
    path('header', HeaderAPIView.as_view(), name='header_api'),
    path('header/add', HeaderAddAPIView.as_view(), name='header_add_api'),
    path('header/delete', HeaderDeleteAPIView.as_view(), name='delete-header'),
    path('footer', FooterAPIView.as_view(), name='footer_api'),
    path('footer/add', FooterAddAPIView.as_view(), name='footer_add_api'),
    path('footer/delete', FooterDeleteAPIView.as_view(), name='delete-footer'),
    path('camera_voice/addCameraVoice', CameraVoiceAPIView.as_view(), name='camera-voice-add'),
    path('camera_voice/getCameraVoiceByID', CameraVoiceAPIView.as_view(), name='camera-voice-by-id'),
    path('camera_voice/getCameraVoiceByCameraID', CameraVoiceByCameraIdAPIView.as_view(), name='camera-voice-by-camera-id'),
    path('camera_voice/getCameraVoice', GetAllCameraVoiceAPIView.as_view(), name='camera-voice-all'),
    path('camera_voice/deleteCameraVoice', DeleteCameraVoiceAPIView.as_view(), name='camera-voice-all'),
    path('camera_voice/updateCameraVoice', UpdateCameraVoiceAPIView.as_view(), name='camera-voice-update'),
    path('camera/getall', CameraAPIView.as_view(), name='camera-voice-update'),
    path('camera/add', CameraAPIView.as_view(), name='camera-add'),
    path('camera/delete', CameraDeleteAPIView.as_view(), name='camera-delete'),
    path('camera/update', CameraUpdateAPIView.as_view(), name='camera-update')
]
