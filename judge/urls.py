from django.urls import path, include
from . import views
from .views import JudgeViewSet

urlpatterns = [
    path('image/', JudgeViewSet.as_view({'post': 'image'}), name='drive'),
    path('image_test/', JudgeViewSet.as_view({'post': 'image_test'}), name='drive')
]
