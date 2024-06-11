from django.urls import path
from .views import ColoringPageListCreateAPIView, ColoringPageDetailAPIView, ColoringPageDeleteAPIView, SendColoringPage

urlpatterns = [
    path('add', ColoringPageListCreateAPIView.as_view(), name='coloringpage_registeration'),
    path('get/all', ColoringPageListCreateAPIView.as_view(), name='get_all_coloring_pages'),
    path('get/<int:pk>', ColoringPageDetailAPIView.as_view(), name='get-coloringpage-by-id'),
    path('delete', ColoringPageDeleteAPIView.as_view(), name='coloringpage_delete'),
    path('update', ColoringPageDetailAPIView.as_view(), name='coloringpage-update'),
    path('sendColoringPDF', SendColoringPage.as_view(), name='coloringpage-update'),
]