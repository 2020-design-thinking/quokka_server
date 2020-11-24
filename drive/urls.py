from django.urls import path, include
from . import views
from .views import DriveViewSet

urlpatterns = [
    path('<int:pk>', DriveViewSet.as_view({
        'get': 'status',
        'put': 'update',
        'delete': 'finish'
    }), name='drive')
]
