from django.urls import path, include
from . import views
from .views import MapDataViewSet

urlpatterns = [
    path('safe_zone', MapDataViewSet.as_view({'get': 'get_safe_zone_list'}), name='map'),
    path('station', MapDataViewSet.as_view({'get': 'get_station_list'}), name='map')
]
