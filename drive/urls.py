from django.urls import path, include
from . import views
from .views import DriveViewSet

urlpatterns = [
    path('<int:pk>/', DriveViewSet.as_view({
        'put': 'update',
        'delete': 'end'
    }), name='drive')
]
