from django.urls import path, include
from . import views
from .views import DeviceViewSet

urlpatterns = [
    path('', DeviceViewSet.as_view({
        'get': 'get_list',
        'post': 'create'
    }), name='devices'),
    path('<int:pk>/', DeviceViewSet.as_view({
        'delete': 'delete',
        'put': 'update'
    }), name='devices'),
    path('<int:pk>/drive', DeviceViewSet.as_view({
        'put': 'drive'
    }), name='devices')
]
